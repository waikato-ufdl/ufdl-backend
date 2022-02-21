from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.jobtypes.base import ServerResidentType
from ufdl.jobtypes.error import TypeParsingException
from ufdl.jobtypes.util import parse_type

from ...exceptions import NotServerResidentType, CouldntParseType, TypeIsAbstract
from ...initialise import initialise
from ...models.jobs import JobType, JobContract
from ._RoutedViewSet import RoutedViewSet


class GetAllValuesOfTypeViewSet(RoutedViewSet):
    """
    Mixin for the job-type view-set which get all server resident values by type.
    """
    # The keyword used to specify when the view-set is in set-file mode
    MODE_KEYWORD: str = "get-all-values-of-type"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/get-all-values/(?P<type_string>.*)$',
                mapping={
                    'get': 'get_all_values_of_type'
                },
                name='{basename}-get-all-values-of-type',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetAllValuesOfTypeViewSet.MODE_KEYWORD}
            )
        ]

    def get_all_values_of_type(self, request: Request, type_string=None):
        """
        Action to get objects with a particular name.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        initialise(JobType, JobContract)

        try:
            type = parse_type(type_string)
        except TypeParsingException as e:
            raise CouldntParseType(e) from e

        if not isinstance(type, ServerResidentType):
            raise NotServerResidentType(type_string)

        if type.is_abstract:
            raise TypeIsAbstract(type_string)

        return Response(type.list_all_values())
