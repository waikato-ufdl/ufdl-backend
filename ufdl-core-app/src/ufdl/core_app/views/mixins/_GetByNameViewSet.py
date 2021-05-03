from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ...models.mixins import filter_by_name
from ._RoutedViewSet import RoutedViewSet


class GetByNameViewSet(RoutedViewSet):
    """
    Mixin for view-sets which can retrieve a model by name.
    """
    # The keyword used to specify when the view-set is in set-file mode
    MODE_KEYWORD: str = "get-by-name"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/(?P<name>.*)$',
                mapping={
                    'get': 'get_by_name'
                },
                name='{basename}-get-by-name',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: GetByNameViewSet.MODE_KEYWORD}
            )
        ]

    def get_by_name(self, request: Request, name=None):
        """
        Action to get objects with a particular name.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the container object.
        :return:            The response containing the file record.
        """
        # Get the set-file object
        query_set = self.get_queryset()

        # Filter to the requested name
        filtered = filter_by_name(query_set, name)

        return Response(self.get_serializer(filtered, many=True).data)
