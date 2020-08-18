from django.db import models

from ...apps import UFDLCoreAppConfig
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
    # The job template the input belongs to
    template = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobTemplate",
                                 on_delete=models.DO_NOTHING,
                                 related_name="inputs")

    # The name of the parameter
    name = models.CharField(max_length=32)

    # The type of value the parameter takes
    type = models.CharField(max_length=32)

    # The default value of the parameter
    options = models.TextField(blank=True, default="")

    # Descriptive help text for user interfaces
    help = models.TextField(blank=True, default="")

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type}" + f" ({self.options})" if self.options != "" else ""

    objects = InputQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each input is distinctly named for a given template
            models.UniqueConstraint(name="unique_template_input_names",
                                    fields=["template", "name"])
        ]
