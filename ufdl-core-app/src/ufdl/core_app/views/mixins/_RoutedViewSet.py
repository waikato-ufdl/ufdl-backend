from typing import Optional, List

from rest_framework import routers
from rest_framework import viewsets


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
