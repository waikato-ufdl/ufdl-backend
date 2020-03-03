from django.urls import path, include

from ufdl.core_app import views as core_views

from .routers import UFDLImageClassificationRouter
from . import views


# Router for routing view-set actions
router = UFDLImageClassificationRouter()
router.register("datasets", views.DatasetViewSet)
router.register("teams", core_views.TeamViewSet)
router.register("projects", core_views.ProjectViewSet)
router.register("users", core_views.UserViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-image-classification-app"
