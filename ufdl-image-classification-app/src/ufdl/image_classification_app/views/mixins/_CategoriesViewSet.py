from typing import List, Tuple

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from ufdl.core_app.exceptions import *
from ufdl.core_app.views.mixins import RoutedViewSet

from ...models.mixins import CategoriesModel


class CategoriesViewSet(RoutedViewSet):
    """
    Mixin for view-sets which allow the adding/removing of categories from files.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "categories"

    @classmethod
    def get_route(cls) -> routers.Route:
        return routers.Route(
            url=r'^{prefix}/{lookup}/categories{trailing_slash}$',
            mapping={'get': 'get_categories',
                     'post': 'add_categories',
                     'delete': 'remove_categories'},
            name='{basename}-categories',
            detail=True,
            initkwargs={cls.MODE_ARGUMENT_NAME: CategoriesViewSet.MODE_KEYWORD}
        )

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
        if not isinstance(dataset, CategoriesModel):
            raise TypeError(f"Object {dataset} is not a categories model")

        # Return the categories
        return Response(dataset.get_categories())

    def add_categories(self, request: Request, pk=None):
        """
        Adds categories to a data-set.

        :param request:     The request containing the category data.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories that were added.
        """
        # Get the image/category lists from the request
        images, categories = self._parse_parameters(request)

        # Get the data-set
        dataset = self.get_object()

        # Make sure the dataset is capable of handling categories
        if not isinstance(dataset, CategoriesModel):
            raise TypeError(f"Object {dataset} is not a categories model")

        # Add the categories to the data-set
        added_categories = dataset.add_categories(images, categories)

        return Response(added_categories)

    def remove_categories(self, request: Request, pk=None):
        """
        Removes categories to a data-set.

        :param request:     The request containing the category data.
        :param pk:          The primary key of the data-set being accessed.
        :return:            The response containing the categories that were removed.
        """
        # Get the image/category lists from the request
        images, categories = self._parse_parameters(request)

        # Get the data-set
        dataset = self.get_object()

        # Make sure the dataset is capable of handling categories
        if not isinstance(dataset, CategoriesModel):
            raise TypeError(f"Object {dataset} is not a categories model")

        # Remove the categories from the data-set
        removed_categories = dataset.remove_categories(images, categories)

        return Response(removed_categories)

    @classmethod
    def _parse_parameters(cls, request: Request) -> Tuple[List[str], List[str]]:
        """
        Parses the parameters for add_categories/remove_categories.

        :param request:     The request containing the parameters.
        :return:            The parameter values, images and categories.
        """
        # Get the parameters
        parameters = dict(request.data)

        # Make sure the images parameter is present
        if "images" not in parameters:
            raise MissingParameter("images")

        # Get the images parameter
        images = parameters.pop("images")

        # Make sure the images is a list of strings
        if not isinstance(images, list) or any(not isinstance(image, str) for image in images):
            raise BadArgumentType("add_categories",
                                  "images",
                                  "list of strings",
                                  images)

        # Make sure the categories parameter is present
        if "categories" not in parameters:
            raise MissingParameter("categories")

        # Get the categories parameter
        categories = parameters.pop("categories")

        # Make sure the categories is a list of strings
        if not isinstance(categories, list) or any(not isinstance(category, str) for category in categories):
            raise BadArgumentType("add_categories",
                                  "categories",
                                  "list of strings",
                                  categories)

        # Make sure there are no other parameters present
        if len(parameters) > 0:
            raise UnknownParameters(parameters)

        return images, categories
