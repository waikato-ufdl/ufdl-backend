from django.urls import path, include

from . import views
from ._UFDLRouter import UFDLRouter


# Router for routing view-set actions
router = UFDLRouter()
router.register("dataassets", views.DataAssetViewSet)
router.register("datasets", views.DatasetViewSet)
router.register("memberships", views.MembershipViewSet)
router.register("teams", views.TeamViewSet)
router.register("projects", views.ProjectViewSet)
router.register("users", views.UserViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# TODO: Explain why this is here
app_name = "ufdl-core-app"