from django.db import models

from ...util import accumulate_delete


class DeleteOnNoRemainingReferencesOnlyQuerySet(models.QuerySet):
    """
    Mixin query-set functionality which makes sure bulk deletes
    check for references first.
    """
    def delete(self):
        # Keep a tally of items deleted
        deletion_accumulator = 0, {}

        # Delete all items in the query-set individually
        for instance in self.all():
           deletion_accumulator = accumulate_delete(deletion_accumulator, instance.delete())

        return deletion_accumulator


class DeleteOnNoRemainingReferencesOnlyModel(models.Model):
    """
    Mixin class that provides the functionality of making sure no
    references exist to the model before it is deleted.
    """
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        # Make sure there are no references to this file anywhere
        for related_object in self._meta.get_fields(include_hidden=True):
            # Skip fields that are not relations
            if not isinstance(related_object, (models.ManyToManyRel, models.ManyToOneRel)):
                continue

            # Get the type of relation
            if related_object.field.many_to_many:
                if self._has_many_to_many_reference(related_object):
                    return self._nothing_deleted()
            elif related_object.field.many_to_one:
                if self._has_many_to_one_reference(related_object):
                    return self._nothing_deleted()
            else:
                # TODO: Extend to handle one-to-many (ForeignKey),
                #       one-to-one (OneToOneField) and many-to-one (???)
                #       relations. For now, error so we know if this occurs.
                raise NotImplementedError("Ref-checked delete on unhandled field type")

        return super().delete(using, keep_parents)

    def _nothing_deleted(self):
        """
        Creates a return value indicating nothing was deleted.

        :return:    The expected return value from delete.
        """
        return 0, {}

    def _has_many_to_many_reference(self, related_object) -> bool:
        """
        Checks if this object is referenced by the related object,
        via a many-to-many relationship.

        :param related_object:  The related object.
        :return:                True if a reference exists.
        """
        # Get the relation field name on the through table
        field = self._get_many_to_many_through_field(related_object)

        # Get the query-set of all entries in the through table
        all_entries = related_object.through._meta.base_manager.all()

        # Filter to just those with a reference to ourselves
        for_us = all_entries.filter(**{field.name: self})

        return for_us.exists()

    @classmethod
    def _get_many_to_many_through_field(cls, related_object):
        """
        Gets the field in the through table that may contain
        a reference to ourselves.

        Based on django.db.models.fields.reverse_related.ManyToManyRel.get_related_field

        :return:    The through-table field.
        """
        opts = related_object.through._meta
        if related_object.through_fields:
            field = opts.get_field(related_object.through_fields[0])
        else:
            for field in opts.fields:
                rel = getattr(field, 'remote_field', None)
                if rel and rel.model == related_object.model:
                    break
        return field

    def _has_many_to_one_reference(self, related_object) -> bool:
        """
        Checks if this object is referenced by the related object,
        via a one-to-many relationship.

        :param related_object:  The related object.
        :return:                True if a reference exists.
        """
        # Get the query-set of all entries in the foreign table
        all_entries = related_object.related_model._meta.base_manager.all()

        # Filter to just those with a reference to ourselves
        for_us = all_entries.filter(**{related_object.field.name: self})

        return for_us.exists()
