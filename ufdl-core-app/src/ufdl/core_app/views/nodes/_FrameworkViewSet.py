from ...models.nodes import Framework
from ...serialisers.nodes import FrameworkSerialiser
from ...permissions import IsAuthenticated, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class FrameworkViewSet(UFDLBaseViewSet):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
    }
