from rest_framework import routers

from .views.mixins import CopyableViewSet, DownloadableViewSet, FileContainerViewSet


class UFDLRouter(routers.DefaultRouter):
    """
    Customised routing for UFDL.
    """
    # Disable DefaultRouter's format suffix style
    include_format_suffixes = False

    routes = routers.DefaultRouter.routes + [
        CopyableViewSet.get_route(),
        DownloadableViewSet.get_route(),
        FileContainerViewSet.get_route()
    ]
