from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ._RoutedViewSet import RoutedViewSet


class PingNodeViewSet(RoutedViewSet):
    """
    Mixin for the node view-set which adds the ability for
    a node to ping the server.
    """
    # The keyword used to specify when the view-set is in ping mode
    MODE_KEYWORD: str = "ping"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/ping{trailing_slash}$',
                mapping={'get': 'ping'},
                name='{basename}-ping',
                detail=False,
                initkwargs={cls.MODE_ARGUMENT_NAME: PingNodeViewSet.MODE_KEYWORD}
            )
        ]

    def ping(self, request: Request):
        """
        Action for a node to ping the server.

        :param request:     The request.
        :return:            An empty response.
        """
        return Response()
