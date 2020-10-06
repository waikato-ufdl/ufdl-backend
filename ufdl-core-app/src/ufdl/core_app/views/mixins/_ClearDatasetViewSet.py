from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ...models import Dataset
from ._RoutedViewSet import RoutedViewSet


class ClearDatasetViewSet(RoutedViewSet):
    """
    Mixin for the data-set view-set which allow the clearing of meta-data/annotations.
    """
    # The keyword used to specify when the view-set is in clear-dataset mode
    MODE_KEYWORD: str = "clear-dataset"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/clear{trailing_slash}$',
                mapping={'delete': 'clear_dataset'},
                name='{basename}-clear-dataset',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: ClearDatasetViewSet.MODE_KEYWORD}
            )
        ]

    def clear_dataset(self, request: Request, pk=None):
        """
        Action to clear a dataset.

        :param request:     The request.
        :param pk:          The primary key of the data-set being cleared.
        :return:            The response containing the new dataset record.
        """
        # Get the data-set
        dataset = self.get_object_of_type(Dataset)

        # Clear it
        dataset.domain_specific.clear()

        return Response(self.get_serializer().to_representation(dataset))
