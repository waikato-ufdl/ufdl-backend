from django.db import models

from ....apps import UFDLCoreAppConfig
from ...mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class MetaTemplateDependencyQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of the dependencies between children of meta-templates.
    """
    pass


class MetaTemplateDependency(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Through-model relating meta-template children to one another.
    """
    # The child that is depended upon for its output
    dependency = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.MetaTemplateChildRelation",
        on_delete=models.DO_NOTHING,
        related_name="dependents"
    )

    # The name/type of the output that is depended upon
    output = models.TextField()

    # The child that depends on the output
    dependent = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.MetaTemplateChildRelation",
        on_delete=models.DO_NOTHING,
        related_name="dependencies"
    )

    # The input of the child template that depends on the output
    input = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Input",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    objects = MetaTemplateDependencyQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each dependency is only stored once
            models.UniqueConstraint(
                name="unique_meta_template_dependencies",
                fields=["dependency", "output", "dependent", "input"]
            )
        ]
