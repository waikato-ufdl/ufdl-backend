from ...models.models import Model
from ...serialisers.models import ModelSerialiser
from ...permissions import IsAuthenticated, AllowNone
from ..mixins import DownloadableViewSet, SetFileViewSet, SoftDeleteViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class ModelViewSet(SetFileViewSet, DownloadableViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "set_file": AllowNone,
        "delete_file": AllowNone,
        "download": IsAuthenticated,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }
