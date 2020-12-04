from django.urls import path, include

from .routers import UFDLImageSegmentationRouter
from . import views


# Router for routing view-set actions
router = UFDLImageSegmentationRouter()
router.register("datasets", views.DatasetViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-image-segmentation-app"
