from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("datasets", views.DatasetViewSet)
router.register("memberships", views.MembershipViewSet)
router.register("organisations", views.OrganisationViewSet)
router.register("projects", views.ProjectViewSet)
router.register("users", views.UserViewSet)

app_name = "ufdl-core-app"
urlpatterns = [
    path('', include(router.urls))
]
