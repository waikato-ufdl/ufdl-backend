from django.urls import path, include

from . import views
from ._UFDLRouter import UFDLRouter


# Router for routing view-set actions
router = UFDLRouter()
router.register("datasets", views.DatasetViewSet)
router.register("teams", views.TeamViewSet)
router.register("projects", views.ProjectViewSet)
router.register("users", views.UserViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-core-app"
