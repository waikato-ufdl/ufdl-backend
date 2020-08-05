from django.db import models

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
    # The name of the parameter
    name = models.CharField(max_length=32)

    # The type of value the parameter takes
    type = models.CharField(max_length=32)

    # The default value of the parameter
    default = models.TextField()

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type} = '{self.default}'"

    objects = ParameterQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each parameter is distinct
            models.UniqueConstraint(name="unique_parameters",
                                    fields=["name", "type", "default"])
        ]
