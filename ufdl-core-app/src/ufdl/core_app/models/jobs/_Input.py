from django.db import models

from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class InputQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of job inputs.
    """
    pass


class Input(DeleteOnNoRemainingReferencesOnlyModel):
    """
    An input to a job template.
    """
    # The name of the parameter
    name = models.CharField(max_length=32)

    # The type of value the parameter takes
    type = models.CharField(max_length=32)

    # The default value of the parameter
    options = models.TextField(blank=True, default="")

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type}" + f" ({self.options})" if self.options != "" else ""

    objects = InputQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each input is distinct
            models.UniqueConstraint(name="unique_inputs",
                                    fields=["name", "type", "options"])
        ]
