from typing import Tuple

from django.db import models

from ufdl.jobtypes.base import UFDLJSONType
from ufdl.jobtypes.util import parse_type

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

    # The types of value the parameter takes (|-separated)
    types = models.TextField()

    # The default value of the parameter
    default = models.TextField(null=True)

    # The type of the default value (uses the first type in 'types' if omitted)
    default_type = models.TextField()

    # Whether the default value is constant
    const = models.BooleanField()

    # Descriptive help text for user interfaces
    help = models.TextField(blank=True, default="")

    objects = ParameterQuerySet.as_manager()

    @property
    def signature(self) -> str:
        return f"{self.name} : {self.type} = '{self.default}'"

    def realise_types(self) -> Tuple[UFDLJSONType, ...]:
        return tuple(
            parse_type(type_string)
            for type_string in self.types.split("|")
        )

    def realise_default_type(self) -> UFDLJSONType:
        return parse_type(self.default_type)

    class Meta:
        constraints = [
            # Ensure that each parameter is distinctly named for a given template
            models.UniqueConstraint(name="unique_template_parameter_names",
                                    fields=["template", "name"])
        ]
