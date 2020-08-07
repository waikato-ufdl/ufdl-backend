from ...models.nodes import DockerImage
from ...serialisers.nodes import DockerImageSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from .._UFDLBaseViewSet import UFDLBaseViewSet


class DockerImageViewSet(UFDLBaseViewSet):
    queryset = DockerImage.objects.all()
    serializer_class = DockerImageSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
