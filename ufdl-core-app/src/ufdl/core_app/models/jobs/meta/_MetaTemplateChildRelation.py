from django.db import models

from ....apps import UFDLCoreAppConfig
from ...mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class MetaTemplateChildRelationQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of the relations between a meta-template and its sub-templates.
    """
    def with_name(self, name: str) -> 'MetaTemplateChildRelationQuerySet':
        """
        Filter to the child-relations with a particular name.

        :param name:
                    The name to filter for.
        :return:
                    The filtered query-set.
        """
        return self.filter(name=name)


class MetaTemplateChildRelation(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Through-model relating meta-templates to their sub-templates.
    """
    # The owning meta-template
    parent = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.MetaTemplate",
        on_delete=models.DO_NOTHING,
        related_name="child_relations"
    )

    # The child template
    child = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.JobTemplate",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    # The name given to the child in the meta-template
    name = models.TextField()

    objects = MetaTemplateChildRelationQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each child is given a different name
            models.UniqueConstraint(name="unique_meta_template_children",
                                    fields=["parent", "name"])
        ]
