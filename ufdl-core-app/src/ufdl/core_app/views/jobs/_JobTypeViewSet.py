from ...models.jobs import JobType
from ...serialisers.jobs import JobTypeSerialiser
from ...permissions import IsAuthenticated, IsAdminUser, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobTypeViewSet(UFDLBaseViewSet):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone
    }
