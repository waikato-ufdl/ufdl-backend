from django.urls import path, include

from . import views
from .routers import UFDLRouter


# Router for routing view-set actions
router = UFDLRouter()
router.register("datasets", views.DatasetViewSet)
router.register("teams", views.TeamViewSet)
router.register("projects", views.ProjectViewSet)
router.register("users", views.UserViewSet)
router.register("licen[cs]es", views.LicenceViewSet)
router.register("log", views.LogEntryViewSet)
router.register("hardware", views.nodes.HardwareViewSet)
router.register("cuda", views.nodes.CUDAVersionViewSet)
router.register("docker", views.nodes.DockerImageViewSet)
router.register("domains", views.DataDomainViewSet)
router.register("frameworks", views.nodes.FrameworkViewSet)
router.register("nodes", views.nodes.NodeViewSet)
router.register("models", views.models.ModelViewSet)
router.register("pretrained-models", views.models.PreTrainedModelViewSet)
router.register("job-types", views.jobs.JobTypeViewSet)
router.register("job-contracts", views.jobs.JobContractViewSet)
router.register("jobs", views.jobs.JobViewSet)
router.register("job-templates", views.jobs.JobTemplateViewSet)
router.register("job-outputs", views.jobs.JobOutputViewSet)

# The final set of URLs routed by this app
urlpatterns = [
    path('', include(router.urls))
]

# Default namespace for the views
app_name = "ufdl-core-app"
