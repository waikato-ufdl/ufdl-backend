from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ._RoutedViewSet import RoutedViewSet


class CopyableViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the copying of model instances.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "copyable"

    @classmethod
    def get_route(cls) -> routers.Route:
        return routers.Route(
            url=r'^{prefix}/{lookup}/copy{trailing_slash}?$',
            mapping={'post': 'copy'},
            name='{basename}-copy',
            detail=True,
            initkwargs={cls.MODE_ARGUMENT_NAME: CopyableViewSet.MODE_KEYWORD}
        )

    def copy(self, request: Request, pk=None):
        """
        Action to copy a dataset.

        :param request:     The request containing the file data.
        :param pk:          The primary key of the dataset being accessed.
        :return:            The response containing the new dataset record.
        """
        # Copy the object
        new_object = self.get_object().copy(creator=request.user, **request.data)

        return Response(self.get_serializer().to_representation(new_object))