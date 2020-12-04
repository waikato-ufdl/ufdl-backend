from ufdl.core_app.routers import UFDLRouter

from ..views.mixins import *


class UFDLImageSegmentationRouter(UFDLRouter):
    """
    Adds the route for adding/removing segmentation images.
    """
    routes = (
            UFDLRouter.routes +
            SegmentationLayersViewSet.get_routes()
    )
