from typing import Optional, Dict

from django.db import models

from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ufdl.json.core.jobs import JobTemplateSpec
from ufdl.json.core.jobs.notification import NotificationOverride

from ...apps import UFDLCoreAppConfig
from ...exceptions import InvalidJobInput
from ...util import max_value
from .._User import User
from ._Input import Input
from ._Job import Job
from ._Parameter import Parameter


class JobTemplateQuerySet(SoftDeleteQuerySet):
    """
    A query-set over job templates.
    """
    def with_name_and_version(self, name: str, version: int):
        """
        Filters the query-set to those instances with a given name and version.

        :param name:        The name of the template.
        :param version:     The template version.
        :return:            The filtered query-set.
        """
        return self.filter(name=name, version=version)

    def max_version(self) -> int:
        """
        Gets the largest version number in all of the job-templates.

        :return:    The version number.
        """
        return max_value(self, "version", 0)


class JobTemplate(SoftDeleteModel):
    """
    A job template.

    TODO: Who owns a job template? A team? A project? The server as a whole?
    """
    # The name of the job template
    name = models.CharField(max_length=200)

    # The version of the job template
    version = models.IntegerField(default=1)

    # A description of the template
    description = models.TextField(blank=True)

    # The scope of the job template
    scope = models.CharField(max_length=16)

    # The licence type for this job template
    licence = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Licence",
        on_delete=models.DO_NOTHING,
        related_name="job_templates"
    )

    # The domain the jobs operate in, if any
    domain = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.DataDomain",
        on_delete=models.DO_NOTHING,
        related_name="job_templates",
        null=True,
        default=None
    )

    @property
    def name_and_version(self) -> str:
        return f"{self.name} v{self.version}"

    objects = JobTemplateQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each input is distinct
            models.UniqueConstraint(name="unique_active_job_templates",
                                    fields=["name", "version"],
                                    condition=SoftDeleteModel.active_Q)
        ]

    def get_input_by_name(self, name: str) -> Optional[Input]:
        """
        Gets an input to this template by name.

        :param name:
                    The name of the input to get.
        :return:
                    The input, or None if it doesn't exist.
        """
        return self.inputs.filter(name=name).first()

    def get_parameter_by_name(self, name: str) -> Optional[Parameter]:
        """
        Gets a parameter to this template by name.

        :param name:
                    The name of the parameter to get.
        :return:
                    The parameter, or None if it doesn't exist.
        """
        return self.parameters.filter(name=name).first()

    def upcast(self) -> 'JobTemplate':
        """
        Up-casts this job template to the specific version, either
        extern or meta.

        :return:
                    The up-casted job-template instance.
        """
        # Already a specific type
        if type(self) is not JobTemplate:
            return self

        if hasattr(self, "workabletemplate"):
            return getattr(self, "workabletemplate")
        else:
            return getattr(self, "metatemplate")

    def check_input_values(
            self,
            input_values: Dict[str, Dict[str, str]]
    ):
        """
        Checks that the input values match the names/types expected
        by this template. Removes any unexpected inputs.

        :param input_values:
                    The input values.
        """
        # Keep a set of known input names
        known_input_names = set()

        # Check each input in turn
        for input in self.inputs.all():
            # Must have a value for the input
            if input.name not in input_values:
                raise InvalidJobInput(
                    f"No input value provided for input '{input.name}'"
                )

            # Get the type of the input
            input_type = input_values[input.name]['type']

            # Must be a valid type for the input
            if input_type not in input.type_list:
                raise InvalidJobInput(
                    f"Input '{input.name}' received value of type {input_type} but expects "
                    f"{input.type_string}"
                )

            # Add the name of the input to the known set
            known_input_names.add(input.name)

        # Get the set of unknown input names
        unknown_input_names = set(input_values.keys())
        unknown_input_names.difference_update(known_input_names)

        # Remove any unknown inputs from the input values
        for input_name in unknown_input_names:
            input_values.pop(input_name)

    def create_job(
            self,
            user: User,
            parent: Optional['Job'],
            input_values: Dict[str, Dict[str, str]],
            parameter_values: Dict[str, str],
            description: Optional[str] = None,
            notification_override: Optional[NotificationOverride] = None,
            child_notification_overrides: Optional[Dict[str, NotificationOverride]] = None
    ) -> Job:
        """
        Creates a new job from this template.

        :param user:
                    The user creating the job.
        :param parent:
                    The parent job if the job is being created as part of a workflow.
        :param input_values:
                    The values provided as input, as a map from the input's name to a
                    {'value': VALUE, 'type': TYPE} object.
        :param parameter_values:
                    The parameter values to the job.
        :param description:
                    A description to help identify the job.
        :param notification_override:
                    The override for this jobs notifications.
        :param child_notification_overrides:
                    The overrides for any children of this job.
        :return:
                    The created job.
        """
        # Call the override on the specific template type (will cause cycle if not overridden properly)
        return self.upcast().create_job(
            user,
            parent,
            input_values,
            parameter_values,
            description,
            notification_override,
            child_notification_overrides
        )

    def to_json(self) -> JobTemplateSpec:
        """
        Formats this job template as a specification for export.

        :return:
                    The JSON specification of this template.
        """
        # Call the override on the specific template type (will cause cycle if not overridden properly)
        return self.upcast().to_json()
