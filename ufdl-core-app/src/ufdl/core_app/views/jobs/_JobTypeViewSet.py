from ...models.jobs import JobType
from ...serialisers.jobs import JobTypeSerialiser
from ...permissions import IsAuthenticated, IsAdminUser
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobTypeViewSet(UFDLBaseViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
