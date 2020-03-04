from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ...json import CategoriesModSpec
from ...models import Dataset


class CategoriesViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the adding/removing of categories from files.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "categories"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/categories{trailing_slash}$',
                mapping={'get': 'get_categories',
                         'post': 'add_categories',
                         'delete': 'remove_categories'},
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
        dataset = self.get_object()

        # Make sure the dataset is capable of handling categories
        if not isinstance(dataset, Dataset):
            raise TypeError(f"Object {dataset} is not a dataset")

        # Return the categories
        return Response(dataset.get_categories().to_raw_json())

    def add_categories(self, request: Request, pk=None):
        """
        Adds categories to a data-set.

        :param request:     The request containing the category data.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories that were added.
        """
        # Get the image/category lists from the request
        mod_spec = self._parse_parameters(request)

        # Get the data-set
        dataset = self.get_object()

        # Make sure the dataset is capable of handling categories
        if not isinstance(dataset, Dataset):
            raise TypeError(f"Object {dataset} is not a dataset")

        return Response(dataset.add_categories(mod_spec.images, mod_spec.categories).to_raw_json())

    def remove_categories(self, request: Request, pk=None):
        """
        Removes categories to a data-set.

        :param request:     The request containing the category data.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories that were removed.
        """
        # Get the image/category lists from the request
        mod_spec = self._parse_parameters(request)

        # Get the data-set
        dataset = self.get_object()

        # Make sure the dataset is capable of handling categories
        if not isinstance(dataset, Dataset):
            raise TypeError(f"Object {dataset} is not a dataset")

        return Response(dataset.remove_categories(mod_spec.images, mod_spec.categories).to_raw_json())

    @classmethod
    def _parse_parameters(cls, request: Request) -> CategoriesModSpec:
        """
        Parses the parameters for add_categories/remove_categories.

        :param request:     The request containing the parameters.
        :return:            The parameter values, images and categories.
        """
        return JSONParseFailure.attempt(dict(request.data), CategoriesModSpec)
