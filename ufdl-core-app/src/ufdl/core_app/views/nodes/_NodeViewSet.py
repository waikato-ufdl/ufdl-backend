from ...models.nodes import Node
from ...serialisers.nodes import NodeSerialiser
from ...permissions import IsAdminUser, IsAuthenticated, NodeIsSelf, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class NodeViewSet(UFDLBaseViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerialiser

    admin_permission_class = AllowNone
    default_permissions = [NodeIsSelf | IsAdminUser]

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "destroy": [AllowNone]
    }
