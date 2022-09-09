from typing import List

from django.db import transaction

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.jobtypes.error import TypeParsingException
from ufdl.jobtypes.util import parse_type

from ufdl.json.core.jobs import CreateJobSpec

from wai.json.object import Absent

from ...exceptions import JSONParseFailure, ChildNotificationOverridesForWorkableJob, CouldntParseType
from ...initialise import initialise
from ...models import JobContract, JobType
from ...models.jobs import JobTemplate, WorkableTemplate
from ...serialisers.jobs import JobSerialiser
from ._RoutedViewSet import RoutedViewSet


class CreateJobViewSet(RoutedViewSet):
    """
    Mixin for the job-template view-set which adds the ability to
    create jobs using the template.
    """
    # The keyword used to specify when the view-set is in create-job mode
    MODE_KEYWORD: str = "create-job"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/create-job{trailing_slash}$',
                mapping={'post': 'create_job'},
                name='{basename}-create-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: CreateJobViewSet.MODE_KEYWORD}
            )
        ]

    @transaction.atomic
    def create_job(self, request: Request, pk=None):
        """
        Action to create a job from the template.

        :param request:     The request containing the job data.
        :param pk:          The primary key of the job template.
        :return:            The response containing the job.
        """
        initialise(JobType, JobContract)

        # Get the job template the job is being created from
        job_template = self.get_object_of_type(JobTemplate).upcast()

        # Parse the job specification from the request
        spec = JSONParseFailure.attempt(dict(request.data), CreateJobSpec)

        # Can't supply child notification overrides to a workable job
        if (
                isinstance(job_template, WorkableTemplate)
                and
                spec.child_notification_overrides is not Absent
        ):
            raise ChildNotificationOverridesForWorkableJob()

        try:
            # Format the input values
            input_values = {
                name: (pair.value, parse_type(pair.type))
                for name, pair in spec.input_values.items()
            }

            # Format the parameter values
            parameter_values = (
                {
                    name: (pair.value, parse_type(pair.type))
                    for name, pair in spec.parameter_values.items()
                } if spec.parameter_values is not Absent
                else None
            )
        except TypeParsingException as e:
            raise CouldntParseType(e) from e

        # Create the job from the template
        job = job_template.create_job(
            request.user,
            None,
            input_values,
            parameter_values,
            spec.description,
            (
                spec.notification_override
                if spec.notification_override is not Absent else
                None
            ),
            (
                spec.child_notification_overrides
                if spec.child_notification_overrides is not Absent else
                None
            )
        )

        return Response(JobSerialiser().to_representation(job))
