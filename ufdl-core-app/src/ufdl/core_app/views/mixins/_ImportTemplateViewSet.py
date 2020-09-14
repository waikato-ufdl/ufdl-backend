from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import JobTemplateMigrationSpec, InputMigrationSpec, ParameterMigrationSpec

from wai.json.object import Absent

from ...exceptions import JSONParseFailure
from ...migrations.job_templates import add_job_template
from ...models import *
from ._RoutedViewSet import RoutedViewSet


class ImportTemplateViewSet(RoutedViewSet):
    """
    Mixin for the job-template view-set which adds the ability
    to import/export job-templates in the migration JSON format.
    """
    # The keyword used to specify when the view-set is in merge mode
    MODE_KEYWORD: str = "import-template"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/import{trailing_slash}$',
                mapping={'post': 'import_template'},
                name='{basename}-import-template',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: ImportTemplateViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/export{trailing_slash}$',
                mapping={'get': 'export_template'},
                name='{basename}-export-template',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: ImportTemplateViewSet.MODE_KEYWORD}
            )
        ]

    def import_template(self, request: Request):
        """
        Action to import a job-template from JSON.

        :param request:     The request containing the job-template JSON.
        :return:            The response containing the job-template.
        """
        # Deserialise the job-template JSON
        spec = JSONParseFailure.attempt(dict(request.data), JobTemplateMigrationSpec)

        # If the template already exists, delete it
        if spec.version is not Absent:
            JobTemplate.objects.with_name_and_version(spec.name, spec.version).active().delete()

        # Add the template
        instance = add_job_template(spec, Input, Parameter, Framework, DataDomain, JobType, Licence, JobTemplate)

        return Response(self.get_serializer().to_representation(instance))

    def export_template(self, request: Request, pk=None):
        """
        Action to export a job-template to JSON.

        :param request:     The request specifying the job-template.
        :param pk:          The primary key of the target job-template.
        :return:            The response containing the job-template JSON.
        """
        # Get the job-template
        job_template = self.get_object_of_type(JobTemplate)

        # Convert it to a JSON message
        json = self.job_template_to_json(job_template)

        return Response(json.to_raw_json())

    def job_template_to_json(self, job_template: JobTemplate) -> JobTemplateMigrationSpec:
        """
        Converts a job-template to a JSON specification.

        :param job_template:    The template to convert.
        :return:                The JSON specification of the template.
        """
        return JobTemplateMigrationSpec(
            name=job_template.name,
            description=job_template.description,
            scope=job_template.scope,
            framework=f"{job_template.framework.name}|{job_template.framework.version}",
            domain=job_template.domain.name,
            job_type=job_template.type.name,
            executor_class=job_template.executor_class,
            required_packages=job_template.required_packages,
            body=job_template.body,
            licence=job_template.licence.name,
            inputs=[InputMigrationSpec(name=input.name, type=input.type, options=input.options, help=input.help)
                    for input in job_template.inputs.all()],
            parameters=[ParameterMigrationSpec(name=parameter.name, type=parameter.type, default=parameter.default, help=parameter.help)
                        for parameter in job_template.parameters.all()]
        )
