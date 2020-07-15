from django.urls import path, include

from . import views
from .routers import UFDLRouter


# Router for routing view-set actions
router = UFDLRouter()
router.register("datasets", views.DatasetViewSet)
router.register("teams", views.TeamViewSet)
router.register("projects", views.ProjectViewSet)
router.register("users", views.UserViewSet)
router.register("licences", views.LicenceViewSet)
router.register("log", views.LogEntryViewSet)
router.register("hardware", views.nodes.HardwareViewSet)
router.register("cuda", views.nodes.CUDAVersionViewSet)
router.register("docker", views.nodes.DockerImageViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-core-app"
