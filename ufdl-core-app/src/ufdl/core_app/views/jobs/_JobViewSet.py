from ...models.jobs import Job
from ...serialisers.jobs import JobSerialiser
from ...permissions import IsAuthenticated, IsAdminUser, NodeOwnsJob, IsNode
from ..mixins import SoftDeleteViewSet, AddJobOutputViewSet, AcquireJobViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobViewSet(AcquireJobViewSet, AddJobOutputViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "add_output": [NodeOwnsJob],
        "acquire_job": [IsNode],
        "start_job": [NodeOwnsJob],
        "finish_job": [NodeOwnsJob]
    }
