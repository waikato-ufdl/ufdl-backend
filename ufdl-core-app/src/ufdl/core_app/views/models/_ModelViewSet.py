from ...models.models import Model
from ...serialisers.models import ModelSerialiser
from ...permissions import IsAdminUser, IsAuthenticated
from ..mixins import DownloadableViewSet, SetFileViewSet, SoftDeleteViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class ModelViewSet(SetFileViewSet, DownloadableViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }