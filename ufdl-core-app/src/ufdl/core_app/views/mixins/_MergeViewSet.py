from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from simple_django_teams.mixins import SoftDeleteModel

from ufdl.json.core import MergeSpec

from ...exceptions import JSONParseFailure
from ...models.mixins import MergableModel
from ._RoutedViewSet import RoutedViewSet


class MergeViewSet(RoutedViewSet):
    """
    Mixin for view-sets to mergable models which adds the ability to merge
    another object into this one.
    """
    # The keyword used to specify when the view-set is in merge mode
    MODE_KEYWORD: str = "merge"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/merge/(?P<other>[^/]+){trailing_slash}$',
                mapping={'post': 'merge'},
                name='{basename}-merge',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: MergeViewSet.MODE_KEYWORD}
            )
        ]

    def merge(self, request: Request, pk=None, other=None):
        """
        Action for an object to merge another object into itself.

        :param request:     The request containing the merge specification.
        :param pk:          The primary key of the target object.
        :param other:       The primary key of the source object.
        :return:            The response containing the merged target object.
        """
        # Get the mergable that is being modified
        target = self.get_object_of_type(MergableModel)

        # Get the source mergable
        source = self.get_object_of_type(MergableModel, other="pk")

        # Deserialise the merge specification
        spec = JSONParseFailure.attempt(dict(request.data), MergeSpec)

        # Perform the merge
        target.merge(source)

        # If specified to delete the source, do so
        if spec.delete:
            if spec.hard and isinstance(source, SoftDeleteModel):
                source.hard_delete()
            else:
                source.delete()

        return Response(self.get_serializer().to_representation(target))
