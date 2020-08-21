from typing import Optional, List, TypeVar, Type

from django.db.models import Model

from rest_framework import routers
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from ...exceptions import BadModelType

# Expected type of model
ModelType = TypeVar("ModelType", bound=Model)


class RoutedViewSet(viewsets.ModelViewSet):
    """
    Base class for view-set mixins which add a route to their
    provided functionality.
    """
    # The name of the init kwarg used to specify the mode of the view-set
    MODE_ARGUMENT_NAME: str = "mode"

    # Read-only access to the mode of the view-set
    mode: Optional[str] = property(lambda self: self._mode)

    def __init__(self, **kwargs):
        # Extract the view-set mode if working in one
        self._mode: Optional[str] = kwargs.pop(self.MODE_ARGUMENT_NAME, None)

        super().__init__(**kwargs)

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        """
        Gets the route for this view-set mixin.

        :return:    The mixin's route.
        """
        raise NotImplementedError(cls.get_routes.__qualname__)

    def get_object_of_type(self, required_type: Type[ModelType], **kwargs) -> ModelType:
        """
        Gets the current object, ensuring it is of the required type of model.

        :param required_type:   The required type of model.
        :return:                The current object.
        """
        # Get the object
        obj = self.get_object() if not kwargs else self.get_object_from_url(**kwargs)

        # Check the object is of the required type
        if not isinstance(obj, required_type):
            raise BadModelType(required_type, type(obj))

        return obj

    def get_object(self):
        return self.get_object_from_url(**{self.lookup_url_kwarg or self.lookup_field: self.lookup_field})

    def get_object_from_url(self, **kwargs):
        """
        Overrides the standard get_object() method to make it more flexible
        (e.g. for when multiple objects are specified in the URL).

        Based on the implementation in rest_framework.generics.GenericAPIView.

        :param kwargs:  Mappings from URL group names to model field.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {}

        for url_group_name, model_field_name in kwargs.items():
            assert url_group_name in self.kwargs, (
                    'Expected view %s to be called with a URL keyword argument '
                    'named "%s". Fix your URL conf, or set the `.lookup_field` '
                    'attribute on the view correctly.' %
                    (self.__class__.__name__, url_group_name)
            )

            filter_kwargs[model_field_name] = self.kwargs[url_group_name]

        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
