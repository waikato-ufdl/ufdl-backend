import json
from typing import Iterator, Optional, Dict, Tuple

from django.db import models

from ufdl.jobcontracts.base import UFDLJobContract
from ufdl.jobcontracts.util import parse_contract

from ufdl.jobtypes.base import UFDLJSONType

from ufdl.json.core.jobs import JobTemplateSpec, WorkableTemplateSpec, InputSpec, ParameterSpec
from ufdl.json.core.jobs.notification import NotificationOverride

from wai.json.object import Absent
from wai.json.raw import RawJSONElement

from .._User import User
from ._Job import Job
from ._JobTemplate import JobTemplate, JobTemplateQuerySet


class WorkableTemplateQuerySet(JobTemplateQuerySet):
    """
    A query-set over externally-worked job templates.
    """
    pass


class WorkableTemplate(JobTemplate):
    """
    An externally-worked job template.
    """
    # The type of the job
    type = models.CharField(max_length=256)

    # The name of the job's Executor class
    executor_class = models.CharField(max_length=128, default="")

    # The dependencies required by the job
    required_packages = models.TextField(blank=True, default="")

    objects = WorkableTemplateQuerySet.as_manager()

    def contract(self) -> UFDLJobContract:
        return parse_contract(self.type)

    def iterate_inputs(self) -> Iterator[Tuple[str, Tuple[UFDLJSONType, ...]]]:
        contract = parse_contract(self.type)

        return (
            (input_name, input.types)
            for input_name, input in contract.inputs.items()
        )

    def create_job(
            self,
            user: User,
            parent: Optional['Job'],
            input_values: Dict[str, Tuple[RawJSONElement, UFDLJSONType]],
            parameter_values: Optional[Dict[str, Tuple[RawJSONElement, UFDLJSONType]]] = None,
            description: Optional[str] = None,
            notification_override: Optional[NotificationOverride] = None,
            child_notification_overrides: Optional[Dict[str, NotificationOverride]] = None
    ) -> Job:
        # Should never pass child notification overrides to a workable job
        assert child_notification_overrides is None, "Workable jobs can't have children"

        # Check all inputs values are present and of a valid type
        if parent is None:
            self.check_input_values(input_values)
            self.check_parameter_values(parameter_values)

        # Create the job instance
        job = Job(
            template=self,
            parent=parent,
            input_values=json.dumps({
                input_name: {
                    "value": input[0],
                    "type": str(input[1])
                }
                for input_name, input in input_values.items()
            }),
            parameter_values=json.dumps({
                parameter_name: {
                    "value": parameter[0],
                    "type": str(parameter[1])
                }
                for parameter_name, parameter in parameter_values.items()
            }) if parameter_values is not None else None,
            description=description if description is not None else "",
            creator=user
        )
        job.save()

        # Attach the notification overrides
        job.set_notifications_from_override(notification_override)

        return job

    def to_json(self) -> JobTemplateSpec:
        return JobTemplateSpec(
            name=self.name,
            version=self.version,
            description=self.description,
            scope=self.scope,
            licence=self.licence.name,
            domain=(
                self.domain.name
                if self.domain is not None else
                Absent
            ),
            specific=WorkableTemplateSpec(
                job_type=self.type.name,
                executor_class=self.executor_class,
                required_packages=self.required_packages,
                body=self.body,
                inputs=[
                    InputSpec(
                        name=input.name,
                        types=input.type_list,
                        options=input.options,
                        help=input.help
                    )
                    for input in self.inputs.all()
                ],
                parameters=[
                    ParameterSpec(
                        name=parameter.name,
                        type=parameter.type,
                        default=parameter.default,
                        help=parameter.help
                    )
                    for parameter in self.parameters.all()
                ]
            )
        )
