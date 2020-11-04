from ...models.nodes import Node
from ...serialisers.nodes import NodeSerialiser
from ...permissions import IsAuthenticated, NodeIsSelf, IsNode
from ..mixins import PingNodeViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class NodeViewSet(PingNodeViewSet, UFDLBaseViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": IsAuthenticated,
        "retrieve": IsAuthenticated,
        "update": NodeIsSelf,
        "partial_update": NodeIsSelf,
        "destroy": NodeIsSelf,
        "ping": IsNode
    }
