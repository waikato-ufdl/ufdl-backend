from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import JobTemplateSpec

from wai.json.object import Absent

from ...exceptions import JSONParseFailure, BadJobTemplate
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
        spec = JSONParseFailure.attempt(dict(request.data), JobTemplateSpec)

        # If the template already exists, delete it
        if spec.version is not Absent:
            JobTemplate.objects.with_name_and_version(spec.name, spec.version).active().delete()

        # Add the template
        try:
            instance = add_job_template(
                spec,
                Parameter,
                Framework,
                DataDomain,
                JobType,
                Licence,
                JobTemplate,
                WorkableTemplate,
                MetaTemplate,
                MetaTemplateChildRelation,
                MetaTemplateDependency
            )
        except Exception as e:
            raise BadJobTemplate(str(e)) from e

        return Response(self.get_serializer().to_representation(instance))

    def export_template(self, request: Request, pk=None):
        """
        Action to export a job-template to JSON.

        :param request:     The request specifying the job-template.
        :param pk:          The primary key of the target job-template.
        :return:            The response containing the job-template JSON.
        """
        # Get the job-template
        job_template = self.get_object_of_type(JobTemplate).upcast()

        return Response(job_template.to_json().to_raw_json())
