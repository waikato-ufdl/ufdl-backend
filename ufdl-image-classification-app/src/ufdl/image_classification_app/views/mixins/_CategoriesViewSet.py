from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ufdl.json.image_classification import CategoriesModSpec

from ...models import ImageClassificationDataset


class CategoriesViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the adding/removing of categories from files.
    """
    # The keyword used to specify when the view-set is in categories mode
    MODE_KEYWORD: str = "categories"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/categories{trailing_slash}$',
                mapping={'get': 'get_categories',
                         'patch': 'modify_categories'},
                name='{basename}-categories',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: CategoriesViewSet.MODE_KEYWORD}
            )
        ]

    def get_categories(self, request: Request, pk=None):
        """
        Gets the categories of a data-set.

        :param request:     The request.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories.
        """
        # Get the data-set
        dataset = self.get_object_of_type(ImageClassificationDataset)

        # Return the categories
        return Response(dataset.get_categories().to_raw_json())

    def modify_categories(self, request: Request, pk=None):
        """
        Modifies categories of a data-set.

        :param request:     The request containing the category data.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories that were added.
        """
        # Get the image/category lists from the request
        mod_spec = self._parse_parameters(request)

        # Get the data-set
        dataset = self.get_object_of_type(ImageClassificationDataset)

        # Get the modification method
        method = dataset.add_categories if mod_spec.method == "add" else dataset.remove_categories

        return Response(method(mod_spec.images, mod_spec.categories).to_raw_json())

    @classmethod
    def _parse_parameters(cls, request: Request) -> CategoriesModSpec:
        """
        Parses the parameters for add_categories/remove_categories.

        :param request:     The request containing the parameters.
        :return:            The parameter values, images and categories.
        """
        return JSONParseFailure.attempt(dict(request.data), CategoriesModSpec)
