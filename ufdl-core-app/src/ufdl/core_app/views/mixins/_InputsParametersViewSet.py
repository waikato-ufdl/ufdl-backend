from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.json.core.jobs import InputSpec, ParameterSpec

from wai.json.object import Absent

from ...exceptions import JSONParseFailure, BadName
from ...models.jobs import JobTemplate, Input, Parameter
from ...serialisers.jobs import InputSerialiser, ParameterSerialiser
from ._RoutedViewSet import RoutedViewSet


class InputsParametersViewSet(RoutedViewSet):
    """
    Mixin for the job template view-set which adds the ability to
    add/remove inputs/parameters from job templates.
    """
    # The keyword used to specify when the view-set is in inputs mode
    INPUTS_MODE_KEYWORD: str = "inputs"

    # The keyword used to specify when the view-set is in parameters mode
    PARAMETERS_MODE_KEYWORD: str = "parameters"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/inputs/(?P<name>.+)$',
                mapping={'post': 'add_input',
                         'delete': 'delete_input'},
                name='{basename}-inputs',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: InputsParametersViewSet.INPUTS_MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/parameters/(?P<name>.+)$',
                mapping={'post': 'add_parameter',
                         'delete': 'delete_parameter'},
                name='{basename}-parameters',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: InputsParametersViewSet.PARAMETERS_MODE_KEYWORD}
            )
        ]

    def add_input(self, request: Request, pk=None, name=None):
        """
        Action to add an input to a job-template.

        :param request:     The request containing the input data.
        :param pk:          The primary key of the job-template.
        :param name:        The name of the input.
        :return:            The response containing the input.
        """
        # Get the job template
        job_template = self.get_object_of_type(JobTemplate)

        # Deserialise the spec from the request
        spec = JSONParseFailure.attempt(dict(request.data), InputSpec)

        # See if the input already exists
        existing = job_template.inputs.filter(name=name).first()

        # If it doesn't exist, create it
        if existing is None:
            existing = Input(template=job_template, name=name, type=spec.type, options=spec.options,
                             help=spec.help if spec.help is not Absent else "")

        # If it does exist, update it
        else:
            existing.type = spec.type
            existing.options = spec.options
            if spec.help is not Absent:
                existing.help = spec.help

        # Save
        existing.save()

        return Response(InputSerialiser().to_representation(existing))

    def delete_input(self, request: Request, pk=None, name=None):
        """
        Action to delete an input from a job-template.

        :param request:     The request.
        :param pk:          The primary key of the job-template.
        :param name:        The name of the input.
        :return:            The response containing the input.
        """
        # Get the job template
        job_template = self.get_object_of_type(JobTemplate)

        # Find the input
        existing = job_template.inputs.filter(name=name).first()

        # Make sure the input exists
        if existing is None:
            raise BadName(name, "Input does not exist on job template")

        # Delete the input
        existing.delete()

        return Response(InputSerialiser().to_representation(existing))

    def add_parameter(self, request: Request, pk=None, name=None):
        """
        Action to add a parameter to a job-template.

        :param request:     The request containing the parameter data.
        :param pk:          The primary key of the job-template.
        :param name:        The name of the parameter.
        :return:            The response containing the parameter.
        """
        # Get the job template
        job_template = self.get_object_of_type(JobTemplate)

        # Deserialise the spec from the request
        spec = JSONParseFailure.attempt(dict(request.data), ParameterSpec)

        # See if the parameter already exists
        existing = job_template.parameters.filter(name=name).first()

        # If it doesn't exist, create it
        if existing is None:
            existing = Parameter(template=job_template, name=name, type=spec.type, default=spec.default,
                                 help=spec.help if spec.help is not Absent else "")

        # If it does exist, update it
        else:
            existing.type = spec.type
            existing.default = spec.default
            if spec.help is not Absent:
                existing.help = spec.help

        # Save
        existing.save()

        return Response(ParameterSerialiser().to_representation(existing))

    def delete_parameter(self, request: Request, pk=None, name=None):
        """
        Action to delete a parameter from a job-template.

        :param request:     The request.
        :param pk:          The primary key of the job-template.
        :param name:        The name of the parameter.
        :return:            The response containing the parameter.
        """
        # Get the job template
        job_template = self.get_object_of_type(JobTemplate)

        # Find the parameter
        existing = job_template.parameters.filter(name=name).first()

        # Make sure the parameter exists
        if existing is None:
            raise BadName(name, "Parameter does not exist on job template")

        # Delete the parameter
        existing.delete()

        return Response(ParameterSerialiser().to_representation(existing))
