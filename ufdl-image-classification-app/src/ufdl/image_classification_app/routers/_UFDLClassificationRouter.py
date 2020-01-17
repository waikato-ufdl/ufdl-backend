from ufdl.core_app.routers import UFDLRouter

from ..views.mixins import *


class UFDLClassificationRouter(UFDLRouter):
    """
    Adds the route for adding/removing categories.
    """
    routes = UFDLRouter.routes + [
        CategoriesViewSet.get_route()
    ]
