from django.urls import path, include

from .routers import UFDLSpectrumClassificationRouter
from . import views


# Router for routing view-set actions
router = UFDLSpectrumClassificationRouter()
router.register("datasets", views.DatasetViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-spectrum-classification-app"
