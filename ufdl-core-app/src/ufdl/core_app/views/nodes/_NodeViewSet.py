from ...models.nodes import Node
from ...serialisers.nodes import NodeSerialiser
from ...permissions import IsAuthenticated, NodeIsSelf, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class NodeViewSet(UFDLBaseViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": IsAuthenticated,
        "retrieve": IsAuthenticated,
        "update": NodeIsSelf,
        "partial_update": NodeIsSelf,
        "destroy": NodeIsSelf
    }
