from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import CreateJobSpec, DockerImageSpec

from wai.json.object import Absent

from ...exceptions import JSONParseFailure, BadArgumentValue
from ...models.jobs import Job, JobTemplate
from ...models.nodes import DockerImage
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

    def create_job(self, request: Request, pk=None):
        """
        Action to create a job from the template.

        :param request:     The request containing the job data.
        :param pk:          The primary key of the job template.
        :return:            The response containing the job.
        """
        # Get the job template the job is being created from
        job_template = self.get_object_of_type(JobTemplate)

        # Parse the job specification from the request
        spec = JSONParseFailure.attempt(dict(request.data), CreateJobSpec)

        # Get the docker image referred to by the spec
        if isinstance(spec.docker_image, DockerImageSpec):
            docker_image = DockerImage.objects.name(spec.docker_image.name).version(spec.docker_image.version).first()
        else:
            docker_image = DockerImage.objects.filter(pk=spec.docker_image).first()

        # If the Docker image doesn't exist, raise an error
        if docker_image is None:
            raise BadArgumentValue(self.action, "docker_image", str(spec.docker_image))

        # Create the job
        job = Job(template=job_template,
                  docker_image=docker_image,
                  input_values=spec.input_values.to_json_string(),
                  parameter_values=(spec.parameter_values.to_json_string()
                                    if spec.parameter_values is not Absent
                                    else ""),
                  creator=request.user)
        job.save()

        return Response(JobSerialiser().to_representation(job))
