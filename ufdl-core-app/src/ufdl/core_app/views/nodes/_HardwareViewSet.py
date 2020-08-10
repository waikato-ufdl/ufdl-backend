from rest_framework.permissions import AllowAny

from ...models.nodes import Hardware
from ...serialisers.nodes import HardwareSerialiser
from ...permissions import IsAdminUser, IsAuthenticated, IsNode
from ..mixins import GetHardwareGenerationViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class HardwareViewSet(GetHardwareGenerationViewSet, UFDLBaseViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "get_hardware_generation": [IsNode]
    }
