from ...models.nodes import Hardware
from ...serialisers.nodes import HardwareSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class HardwareViewSet(UFDLBaseViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
