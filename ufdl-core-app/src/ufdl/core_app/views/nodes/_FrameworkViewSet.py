from ...models.nodes import Framework
from ...serialisers.nodes import FrameworkSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class FrameworkViewSet(UFDLBaseViewSet):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
