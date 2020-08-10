from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

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

        # Make sure the user acquiring the job is a node
        if not isinstance(request.user, User) or request.user.node is None:
            raise Exception(f"Non-node user attempted to acquire job: {request.user}")

        # Allow the node to acquire the job
        job.node = request.user.node
        job.save(update_fields=['node'])

        return Response(JobSerialiser().to_representation(job))
