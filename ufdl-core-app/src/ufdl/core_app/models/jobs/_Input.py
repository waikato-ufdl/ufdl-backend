from typing import List

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
    name = models.TextField()

    # The type of value the parameter takes
    types = models.TextField()

    # The default value of the parameter
    options = models.TextField(blank=True, default="")

    # Descriptive help text for user interfaces
    help = models.TextField(blank=True, default="")

    @property
    def type_list(self) -> List[str]:
        """
        A list of the possible types of this input.
        """
        return self.types.split("\n")

    @property
    def type_string(self) -> str:
        """
        A string-representation of the types of this input.
        """
        # Get the list of possible types
        types = self.type_list

        # Format the types into a string
        return (
            f"Union[{', '.join(types)}]"
            if len(types) > 1 else
            types[0]
        )

    @property
    def signature(self) -> str:
        """
        The signature of the input.
        """
        return (
            f"{self.name} : {self.type_string}"
            if self.options == "" else
            f"{self.name} : {self.type_string} ({self.options})"
        )

    objects = InputQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each input is distinctly named for a given template
            models.UniqueConstraint(name="unique_template_input_names",
                                    fields=["template", "name"])
        ]
