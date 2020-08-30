from ...models.nodes import CUDAVersion
from ...serialisers.nodes import CUDAVersionSerialiser
from ...permissions import IsAuthenticated, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class CUDAVersionViewSet(UFDLBaseViewSet):
    queryset = CUDAVersion.objects.all()
    serializer_class = CUDAVersionSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone
    }
