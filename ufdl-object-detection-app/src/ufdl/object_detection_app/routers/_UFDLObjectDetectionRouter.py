from ufdl.core_app.routers import UFDLRouter

from ..views.mixins import *


class UFDLObjectDetectionRouter(UFDLRouter):
    """
    Adds the route for adding/removing categories.
    """
    routes = UFDLRouter.routes + AnnotationsViewSet.get_routes()
