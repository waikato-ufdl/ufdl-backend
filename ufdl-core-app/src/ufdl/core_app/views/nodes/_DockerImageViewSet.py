from ...models.nodes import DockerImage
from ...serialisers.nodes import DockerImageSerialiser
from ...permissions import IsAuthenticated, AllowNone
from .._UFDLBaseViewSet import UFDLBaseViewSet


class DockerImageViewSet(UFDLBaseViewSet):
    queryset = DockerImage.objects.all()
    serializer_class = DockerImageSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone
    }
