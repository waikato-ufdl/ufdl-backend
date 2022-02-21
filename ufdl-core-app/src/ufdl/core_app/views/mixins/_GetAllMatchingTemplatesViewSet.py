import json
from typing import Dict, List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.jobcontracts.util import parse_contract

from ufdl.jobtypes.base import UFDLType
from ufdl.jobtypes.error import TypeParsingException
from ufdl.jobtypes.util import parse_type

from ...exceptions import BadModelType, BadName, CouldntParseType
from ...initialise import initialise
from ...models.jobs import JobType, JobContract, WorkableTemplate, JobTemplate
from ._RoutedViewSet import RoutedViewSet


class GetAllMatchingTemplatesViewSet(RoutedViewSet):
    """
    Mixin for the job-template view-set which gets all templates that can take inputs
    of given types.
    """
    # The keyword used to specify when the view-set is in set-file mode
    MODE_KEYWORD: str = "get-all-matching-templates"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/get-all-matching-templates/(?P<contract_name>.*)$',
                mapping={
                    'get': 'get_all_matching_templates'
                },
                name='{basename}-get-all-matching-templates',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetAllMatchingTemplatesViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/get-all-parameters$',
                mapping={
                    'get': 'get_all_parameters'
                },
                name='{basename}-get-all-parameters',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetAllMatchingTemplatesViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/get-types$',
                mapping={
                    'get': 'get_types'
                },
                name='{basename}-get-types',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetAllMatchingTemplatesViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/get-outputs',
                mapping={
                    'get': 'get_outputs'
                },
                name='{basename}-get-outputs',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetAllMatchingTemplatesViewSet.MODE_KEYWORD}
            )
        ]

    def get_all_matching_templates(self, request: Request, contract_name=None):
        """
        TODO

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        initialise(JobType, JobContract)

        # Parse the contract name
        contract_instance: JobContract = JobContract.objects.filter(name=contract_name).first()
        if contract_instance is None:
            raise BadName(contract_name, "Unknown contract name")
        contract_type = contract_instance.realise_cls()

        # Parse the input types
        try:
            input_types: Dict[str, UFDLType] = {
                param: parse_type(value)
                for param, value in request.query_params.items()
            }
        except TypeParsingException as e:
            raise CouldntParseType(e) from e

        # Make sure the input names are valid
        for input_name in input_types:
            if input_name not in contract_type.input_constructors():
                raise BadName(input_name, f"Not an input to {contract_name}")

        # Search for all job-templates which can take the given inputs
        matching_templates = []
        for job_template in self.get_queryset():
            job_template = job_template.upcast()
            if isinstance(job_template, WorkableTemplate):
                contract = parse_contract(job_template.type)
                if not isinstance(contract, contract_type):
                    continue
                if all(
                    any(
                        input_type.is_subtype_of(contract_input_type)
                        for contract_input_type in contract.inputs[input_name].types
                    )
                    for input_name, input_type in input_types.items()
                ):
                    matching_templates.append(job_template)

        return Response(
            [
                self.get_serializer().to_representation(job_template)
                for job_template in matching_templates
            ]
        )

    def get_all_parameters(self, request: Request, pk=None):
        """
        TODO

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        initialise(JobType, JobContract)

        template = self.get_object_of_type(JobTemplate).upcast()

        parameters = {}
        for parameter in template.parameters.all():
            parameter_json = {
                "types": {
                    parameter_type: parse_type(parameter_type).json_schema
                    for parameter_type in parameter.types.split("|")
                },
                "help": parameter.help
            }

            if parameter.default is not None:
                parameter_json["default"] = {
                    "value": json.loads(parameter.default),
                    "type": parameter.default_type,
                    "schema": parse_type(parameter.default_type).json_schema,
                    "const": parameter.const
                }

            parameters[parameter.name] = parameter_json

        return Response(parameters)

    def get_types(self, request: Request, pk=None):
        """
        TODO

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        initialise(JobType, JobContract)

        template = self.get_object_of_type(JobTemplate).upcast()
        template.upcast()
        if not isinstance(template, WorkableTemplate):
            raise BadModelType(WorkableTemplate, type(template))

        contract = template.contract()

        return Response({
            str(name): str(contract_type)
            for name, contract_type in contract.types.items()
        })

    def get_outputs(self, request: Request, pk=None):
        """
        TODO

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        initialise(JobType, JobContract)

        template = self.get_object_of_type(JobTemplate).upcast()
        template.upcast()
        if not isinstance(template, WorkableTemplate):
            raise BadModelType(WorkableTemplate, type(template))

        contract = template.contract()

        return Response({
            name: str(output.type)
            for name, output in contract.outputs.items()
        })
