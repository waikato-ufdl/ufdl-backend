from ...models.nodes import Node
from ...serialisers.nodes import NodeSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class NodeViewSet(UFDLBaseViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated]
    }
