from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from simple_django_teams.mixins import SoftDeleteModel

from ._RoutedViewSet import RoutedViewSet


class SoftDeleteViewSet(RoutedViewSet):
    """
    Mixin view-set for soft-delete models. Soft-delete models override the
    normal delete method to simply add a "deletion time" to indicate that
    they have been deleted. This mixin adds the ability to "un-delete" these
    models again, and also hard-delete them.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "soft-delete"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/hard{trailing_slash}$',
                mapping={'delete': 'hard_delete'},
                name='{basename}-hard-delete',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: SoftDeleteViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/reinstate{trailing_slash}$',
                mapping={'delete': 'reinstate'},
                name='{basename}-reinstate',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: SoftDeleteViewSet.MODE_KEYWORD}
            )
        ]

    def hard_delete(self, request: Request, pk=None):
        """
        Permanently deletes an instance of a soft-delete model.

        :param request:     The request.
        :param pk:          The primary key of the object to delete.
        :return:            The instance that was deleted.
        """
        # Get the soft-delete object
        obj = self.get_object_of_type(SoftDeleteModel)

        # Perform the hard-delete
        obj.hard_delete()

        return Response(self.get_serializer().to_representation(obj))

    def reinstate(self, request: Request, pk=None):
        """
        Reinstates a formerly soft-deleted object.

        :param request:     The request.
        :param pk:          The primary key of the object to reinstate.
        :return:            The instance that was reinstated.
        """
        # Get the soft-delete object
        obj = self.get_object_of_type(SoftDeleteModel)

        # Perform the reinstatement
        obj.reinstate()

        return Response(self.get_serializer().to_representation(obj))
