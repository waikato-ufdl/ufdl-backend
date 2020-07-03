from rest_framework import routers

from ..views.mixins import *


class UFDLRouter(routers.DefaultRouter):
    """
    Customised routing for UFDL.
    """
    # Disable DefaultRouter's format suffix style
    include_format_suffixes = False

    # Make routes with and without trailing slashes work
    trailing_slash = property(lambda self: "/?", lambda self, value: None)

    routes = (
            routers.DefaultRouter.routes +
            CopyableViewSet.get_routes() +
            DownloadableViewSet.get_routes() +
            FileContainerViewSet.get_routes() +
            MembershipViewSet.get_routes() +
            LicenceSubdescriptorViewSet.get_routes() +
            SoftDeleteViewSet.get_routes()
    )
