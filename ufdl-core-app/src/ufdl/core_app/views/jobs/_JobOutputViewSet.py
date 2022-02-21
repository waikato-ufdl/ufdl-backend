from ...models.jobs import JobOutput
from ...serialisers.jobs import JobOutputSerialiser
from ...permissions import IsAuthenticated, AllowNone, IsAdminUser
from ..mixins import SoftDeleteViewSet, DownloadableViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobOutputViewSet(DownloadableViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = JobOutput.objects.all()
    serializer_class = JobOutputSerialiser

    admin_permission_class = AllowNone

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": IsAdminUser,
        "hard_delete": IsAdminUser,
        "reinstate": IsAdminUser,
        "download": IsAuthenticated
    }
