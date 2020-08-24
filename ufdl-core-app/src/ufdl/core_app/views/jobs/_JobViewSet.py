from ...models.jobs import Job
from ...serialisers.jobs import JobSerialiser
from ...permissions import IsAuthenticated, IsAdminUser, NodeOwnsJob, IsNode, AllowNone
from ..mixins import SoftDeleteViewSet, AddJobOutputViewSet, AcquireJobViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobViewSet(AcquireJobViewSet, AddJobOutputViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerialiser

    admin_permission_class = AllowNone  # Some actions require the admin is a node, so must be explicit

    permission_classes = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [IsAdminUser],
        "partial_update": [IsAdminUser],
        "destroy": [IsAdminUser],
        "add_output": [IsAdminUser | NodeOwnsJob],
        "acquire_job": [IsNode],
        "start_job": [NodeOwnsJob],
        "finish_job": [NodeOwnsJob]
    }
