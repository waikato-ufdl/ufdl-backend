from typing import List

from rest_framework import routers
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response

from ...exceptions import BadName
from ...models.files import File
from ...models.jobs import Job, JobOutput
from ...renderers import BinaryFileRenderer
from ...serialisers.jobs import JobOutputSerialiser
from ._RoutedViewSet import RoutedViewSet


class AddJobOutputViewSet(RoutedViewSet):
    """
    Mixin for the job view-set which adds the ability to
    add outputs to the job.
    """
    # The keyword used to specify when the view-set is in add-outputs mode
    MODE_KEYWORD: str = "add-job-output"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/outputs/(?P<name>[^/]+)/?(?P<type>[^/]*)$',
                mapping={'post': 'add_output',
                         'delete': 'delete_output',
                         'get': 'get_output'},
                name='{basename}-job-outputs',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: AddJobOutputViewSet.MODE_KEYWORD}
            )
        ]

    def get_parsers(self):
        # If not posting a file, return the standard parsers
        if self.mode != AddJobOutputViewSet.MODE_KEYWORD or self.request.method != 'POST':
            return super().get_parsers()

        return [FileUploadParser()]

    def get_renderers(self):
        # If not getting a file, return the standard renderers
        if self.mode != AddJobOutputViewSet.MODE_KEYWORD or self.request.method != 'GET':
            return super().get_renderers()

        return [BinaryFileRenderer()]

    def add_output(self, request: Request, pk=None, name=None, type=None):
        """
        Action to add an output to a job.

        :param request:     The request containing the output data.
        :param pk:          The primary key of the job.
        :param name:        The name of the output.
        :param type:        The type of the output.
        :return:            The response containing the output.
        """
        # Get the job the output is being added to
        job = self.get_object_of_type(Job)

        # Make sure the job doesn't already have an output by this name
        if job.outputs.filter(name=name).exists():
            raise BadName(name, "Job already has an output by this name")

        # If no type is given, use the empty string
        if type is None:
            type = ""

        # Read the data from the request
        data = request.data['file'].file.read()

        # Create the output
        output = JobOutput(job=job, name=name, type=type, data=File.get_reference_from_backend(data), creator=request.user)
        output.save()

        return Response(JobOutputSerialiser().to_representation(output))

    def delete_output(self, request: Request, pk=None, name=None, type=None):
        """
        Action to set the type of an output to a job.

        :param request:     The request containing the output type.
        :param pk:          The primary key of the job.
        :param name:        The name of the output.
        :param type:        The type of the output.
        :return:            The response containing the output.
        """
        # Get the job the output belongs to
        job = self.get_object_of_type(Job)

        # Get the named output
        output = job.outputs.filter(name=name).first()

        # Make sure the output exists
        if output is None:
            raise BadName(name, "Job has no output by this name")

        # Delete the output
        output.delete()

        return Response(JobOutputSerialiser().to_representation(output))

    def get_output(self, request: Request, pk=None, name=None, type=None):
        """
        Action to get the data from a job output.

        :param request:     The request.
        :param pk:          The primary key of the job.
        :param name:        The name of the output.
        :param type:        The type of the output.
        :return:            The response containing the output data.
        """
        # Get the job the output belongs to
        job = self.get_object_of_type(Job)

        # Get the named output
        output = job.outputs.filter(name=name).first()

        # Make sure the output exists
        if output is None:
            raise BadName(name, "Job has no output by this name")

        return Response(output.data.get_data())
