from ...models.nodes import Hardware
from ...serialisers.nodes import HardwareSerialiser
from ...permissions import IsAdminUser, IsAuthenticated, AllowNone
from ..mixins import GetHardwareGenerationViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class HardwareViewSet(GetHardwareGenerationViewSet, UFDLBaseViewSet):
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "get_hardware_generation": IsAuthenticated
    }
