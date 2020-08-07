from ...models.nodes import Node
from ...serialisers.nodes import NodeSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class NodeViewSet(UFDLBaseViewSet):
    # TODO: Need to rethink permissions. Should there be a special node user type?
    queryset = Node.objects.all()
    serializer_class = NodeSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
