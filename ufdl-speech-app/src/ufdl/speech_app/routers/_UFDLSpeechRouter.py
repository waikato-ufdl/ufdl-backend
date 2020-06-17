from ufdl.core_app.routers import UFDLRouter

from ..views.mixins import *


class UFDLSpeechRouter(UFDLRouter):
    """
    Adds the route for setting transcriptions.
    """
    routes = (
            UFDLRouter.routes +
            TranscriptionsViewSet.get_routes()
    )
