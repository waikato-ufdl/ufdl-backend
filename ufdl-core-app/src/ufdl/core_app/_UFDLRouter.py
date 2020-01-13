from rest_framework import routers

from .views.mixins import AS_FILE_KWARG


class UFDLRouter(routers.DefaultRouter):
    """
    Customised routing for UFDL.
    """
    # Disable DefaultRouter's format suffix style
    include_format_suffixes = False

    routes = routers.DefaultRouter.routes + [
        routers.Route(
            url=r'^{prefix}/{lookup}/download$',
            mapping={'get': 'as_file'},
            name='{basename}-as-file',
            detail=True,
            initkwargs={AS_FILE_KWARG: True}
        )
    ]
