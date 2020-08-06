from ...models.nodes import CUDAVersion
from ...serialisers.nodes import CUDAVersionSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class CUDAVersionViewSet(UFDLBaseViewSet):
    queryset = CUDAVersion.objects.all()
    serializer_class = CUDAVersionSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
