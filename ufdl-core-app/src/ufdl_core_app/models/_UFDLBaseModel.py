from django.db import models
from django.utils.timezone import now

from ..apps import APP_NAME


class UFDLBaseQuerySet(models.QuerySet):
    """
    Base class for query-sets of soft-delete models.
    """
    def active(self):
        """
        Filters the query-set to only those that are active.
        """
        return self.filter(deletion_time__isnull=True)

    def deleted(self):
        """
        Filters the query-set to those that are deleted.
        """
        return self.filter(deletion_time__isnull=False)

    def pre_delete(self):
        """
        Can be overridden to perform other actions before
        the models are deleted.
        """
        pass

    def delete(self):
        # Only delete active models
        active = self.active()

        # Perform any pre-delete actions
        active.pre_delete()

        # Set the deletion time of the active models
        active.update(deletion_time=now())


class UFDLBaseModel(models.Model):
    """
    Base class for models that don't actually get deleted from the
    database, instead recording a deletion time.
    """
    # The user that created the object
    creator = models.ForeignKey(f"{APP_NAME}.User",
                                on_delete=models.DO_NOTHING,
                                related_name="+",
                                editable=False)

    # The creation date/time of the object
    creation_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    # The deletion time of the object. A value of null means it hasn't been deleted
    deletion_time = models.DateTimeField(null=True,
                                         default=None,
                                         editable=False)

    # Q object for filtering active and deleted models
    active_Q = models.Q(deletion_time__isnull=True)
    deleted_Q = models.Q(deletion_time__isnull=False)

    class Meta:
        abstract = True

    def is_active(self) -> bool:
        """
        Whether the model is still active (not deleted).
        """
        return self.deletion_time is None

    def is_deleted(self) -> bool:
        """
        Whether the model has been deleted.\
        """
        return not self.is_active()

    def pre_delete(self):
        """
        Can be overridden to perform other actions before
        the models are deleted.
        """
        pass

    def delete(self, using=None, keep_parents=False):
        # Can't delete the deleted
        if self.is_deleted():
            return

        # Perform pre-delete actions
        self.pre_delete()

        # Set the deletion time
        self.deletion_time = now()

        self.save(update_fields=["deletion_time"])
