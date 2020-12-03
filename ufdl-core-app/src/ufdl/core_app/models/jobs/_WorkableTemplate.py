import json
from typing import Optional, Dict

from django.db import models

from ufdl.json.core.jobs import JobTemplateSpec, WorkableTemplateSpec, InputSpec, ParameterSpec
from ufdl.json.core.jobs.notification import NotificationOverride

from wai.json.object import Absent

from ...apps import UFDLCoreAppConfig
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
    # The framework the job works with
    framework = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Framework",
        on_delete=models.DO_NOTHING,
        related_name="job_templates"
    )

    # The type of the job
    type = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.JobType",
        on_delete=models.DO_NOTHING,
        related_name="job_templates"
    )

    # The name of the job's Executor class
    executor_class = models.CharField(max_length=128, default="")

    # The dependencies required by the job
    required_packages = models.TextField(blank=True, default="")

    # The body of the job template itself (interpreted by the Executor class)
    body = models.TextField(default="")

    objects = WorkableTemplateQuerySet.as_manager()

    def create_job(
            self,
            user: User,
            parent: Optional[Job],
            input_values: Dict[str, Dict[str, str]],
            parameter_values: Dict[str, str],
            description: Optional[str] = None,
            notification_override: Optional[NotificationOverride] = None,
            child_notification_overrides: Optional[Dict[str, NotificationOverride]] = None
    ) -> Job:
        # Should never pass child notification overrides to a workable job
        assert child_notification_overrides is None, "Workable jobs can't have children"

        # Check all inputs values are present and of a valid type
        if parent is None:
            self.check_input_values(input_values)

        # Create the job instance
        job = Job(
            template=self,
            parent=parent,
            input_values=json.dumps(input_values),
            parameter_values=json.dumps(parameter_values),
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
            remaining=WorkableTemplateSpec(
                framework=self.framework.signature,
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
                    for input in self.inputs
                ],
                parameters=[
                    ParameterSpec(
                        name=parameter.name,
                        type=parameter.type,
                        default=parameter.default,
                        help=parameter.help
                    )
                    for parameter in self.parameters]
            )
        )
