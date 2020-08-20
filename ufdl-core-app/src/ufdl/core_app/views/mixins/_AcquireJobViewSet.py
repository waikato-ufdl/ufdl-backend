from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import StartJobSpec, FinishJobSpec

from wai.json.object import Absent

from ...exceptions import *
from ...models import User
from ...models.jobs import Job
from ...serialisers.jobs import JobSerialiser
from ._RoutedViewSet import RoutedViewSet


class AcquireJobViewSet(RoutedViewSet):
    """
    Mixin for the job view-set which adds the ability for nodes
    to acquire the job.
    """
    # The keyword used to specify when the view-set is in acquire-job mode
    MODE_KEYWORD: str = "acquire-job"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/acquire{trailing_slash}$',
                mapping={'get': 'acquire_job'},
                name='{basename}-acquire-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/start{trailing_slash}$',
                mapping={'post': 'start_job'},
                name='{basename}-start-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/finish{trailing_slash}$',
                mapping={'post': 'finish_job'},
                name='{basename}-finish-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            )
        ]

    def acquire_job(self, request: Request, pk=None):
        """
        Action for a node to acquire a job.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :return:            The response containing the job.
        """
        # Get the job that is being acquired
        job = self.get_object_of_type(Job)

        # Make sure the job isn't already acquired
        if job.is_acquired:
            raise JobAcquired()

        # Make sure the user acquiring the job is a node
        if not isinstance(request.user, User) or request.user.node is None:
            raise Exception(f"Non-node user attempted to acquire job: {request.user}")

        # Allow the node to acquire the job
        job.node = request.user.node
        job.save(update_fields=['node'])

        return Response(JobSerialiser().to_representation(job))

    def start_job(self, request: Request, pk=None):
        """
        Action for a node to start a job.

        :param request:     The request containing the start-job specification.
        :param pk:          The primary key of the job.
        :return:            The response containing the job.
        """
        # Get the job that is being acquired
        job = self.get_object_of_type(Job)

        # Make sure the job hasn't already been started
        if job.is_started:
            raise JobStarted(self.action)

        # Make sure the user acquiring the job is a node
        if not isinstance(request.user, User) or request.user.node is None:
            raise Exception(f"Non-node user attempted to start job: {request.user}")

        # Get the node reference
        node = request.user.node

        # Make sure the node isn't already working a job
        if node.is_working_job:
            raise NodeAlreadyWorking()

        # Parse the start-job specification (currently unused)
        start_job_spec = JSONParseFailure.attempt(dict(request.data), StartJobSpec)

        # Start the job
        job.start()

        # Set the node's current job
        node.current_job = job
        node.save(update_fields=["current_job"])

        return Response(JobSerialiser().to_representation(job))

    def finish_job(self, request: Request, pk=None):
        """
        Action for a node to finish a job.

        :param request:     The request containing the finish-job specification.
        :param pk:          The primary key of the job.
        :return:            The response containing the job.
        """
        # Get the job that is being acquired
        job = self.get_object_of_type(Job)

        # Make sure the job has been started
        if not job.is_started:
            raise JobNotStarted(self.action)

        # Make sure the job isn't already finished
        if job.is_finished:
            raise JobFinished(self.action)

        # Make sure the user acquiring the job is a node
        if not isinstance(request.user, User) or request.user.node is None:
            raise Exception(f"Non-node user attempted to start job: {request.user}")

        # Get the node reference
        node = request.user.node

        # Parse the finish-job specification
        finish_job_spec = JSONParseFailure.attempt(dict(request.data), FinishJobSpec)

        # Finish the job
        error = finish_job_spec.error
        job.finish(error if error is not Absent else None)

        # Clear the current job from the node
        node.current_job = None
        node.save(update_fields=["current_job"])

        return Response(JobSerialiser().to_representation(job))
