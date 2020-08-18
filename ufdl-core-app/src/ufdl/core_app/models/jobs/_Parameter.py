from django.db import models

from ...apps import UFDLCoreAppConfig
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class ParameterQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of job parameters.
    """
    pass


class Parameter(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A parameter to a job template.
    """
    # The job template the input belongs to
    template = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobTemplate",
                                 on_delete=models.DO_NOTHING,
                                 related_name="parameters")

    # The name of the parameter
    name = models.CharField(max_length=32)

    # The type of value the parameter takes
    type = models.CharField(max_length=32)

    # The default value of the parameter
    default = models.TextField()

    # Descriptive help text for user interfaces
    help = models.TextField(blank=True, default="")

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type} = '{self.default}'"

    objects = ParameterQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each parameter is distinctly named for a given template
            models.UniqueConstraint(name="unique_template_parameter_names",
                                    fields=["template", "name"])
        ]
