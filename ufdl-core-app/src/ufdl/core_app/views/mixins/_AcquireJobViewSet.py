from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import StartJobSpec, FinishJobSpec

from wai.json.object import Absent

from ...exceptions import *
from ...models.jobs import Job
from ...models.nodes import Node
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
                url=r'^{prefix}/{lookup}/release{trailing_slash}$',
                mapping={'delete': 'release_job'},
                name='{basename}-release-job',
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
                url=r'^{prefix}/{lookup}/progress/(?P<progress>(0.[0-9]+)|(1.(0)+)){trailing_slash}$',
                mapping={'post': 'progress_job'},
                name='{basename}-progress-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/finish{trailing_slash}$',
                mapping={'post': 'finish_job'},
                name='{basename}-finish-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/reset{trailing_slash}$',
                mapping={'delete': 'reset_job'},
                name='{basename}-reset-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/abort{trailing_slash}$',
                mapping={'delete': 'abort_job'},
                name='{basename}-abort-job',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AcquireJobViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/cancel{trailing_slash}$',
                mapping={'delete': 'cancel_job'},
                name='{basename}-cancel-job',
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

        # Get the node making the request
        node = Node.from_request(request)

        # Allow the node to acquire the job
        job.acquire(node)

        return Response(JobSerialiser().to_representation(job))

    def release_job(self, request: Request, pk=None):
        """
        Action for a node to release a job.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :return:            The response containing the job.
        """
        # Get the job that is being acquired
        job = self.get_object_of_type(Job)

        # Allow the node to acquire the job
        job.release()

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

        # Get the node making the request
        node = Node.from_request(request)

        # Parse the start-job specification (currently unused)
        start_job_spec = JSONParseFailure.attempt(dict(request.data), StartJobSpec)

        # Start the job
        job.start(node)

        return Response(JobSerialiser().to_representation(job))

    def progress_job(self, request: Request, pk=None, progress=None):
        """
        Action for a node to update the progress of a job.

        :param request:
                    The request containing the progress-job specification.
        :param pk:
                    The primary key of the job.
        :param progress:
                    The amount of progress ma
        :return:
                    A response containing the job.
        """
        # Get the job that is being updated
        job = self.get_object_of_type(Job)

        # Get the node making the request
        node = Node.from_request(request)

        # Parse the progress amount
        progress_amount = float(progress)

        # Parse the progress-job specification
        progress_job_spec = dict(request.data)

        # Progress the job
        job.progress(node, progress_amount, **progress_job_spec)

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

        # Get the node making the request
        node = Node.from_request(request)

        # Parse the finish-job specification
        finish_job_spec = JSONParseFailure.attempt(dict(request.data), FinishJobSpec)

        # Finish the job
        error = finish_job_spec.error
        if error is Absent:
            job.finish(node)
        else:
            job.error(node, error)

        return Response(JobSerialiser().to_representation(job))

    def reset_job(self, request: Request, pk=None):
        """
        Action to reset a job.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :return:            The response containing the job, after reset.
        """
        # Get the job that is being reset
        job = self.get_object_of_type(Job)

        # Reset the job
        job.reset()

        return Response(JobSerialiser().to_representation(job))

    def abort_job(self, request: Request, pk=None):
        """
        Action to abort a job.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :return:            The response containing the job, after abort.
        """
        # Get the job that is being reset
        job = self.get_object_of_type(Job)

        # Reset the job
        job.abort()

        return Response(JobSerialiser().to_representation(job))

    def cancel_job(self, request: Request, pk=None):
        """
        Action to cancel a job.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :return:            The response containing the job, after cancellation.
        """
        # Get the job that is being cancelled
        job = self.get_object_of_type(Job)

        # Cancel the job
        job.cancel()

        return Response(JobSerialiser().to_representation(job))
