from ...models.jobs import JobContract
from ...serialisers.jobs import JobContractSerialiser
from ...permissions import IsAuthenticated, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobContractViewSet(UFDLBaseViewSet):
    queryset = JobContract.objects.all()
    serializer_class = JobContractSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone
    }
