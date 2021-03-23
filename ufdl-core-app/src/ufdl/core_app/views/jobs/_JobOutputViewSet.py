from ...models.jobs import JobOutput
from ...serialisers.jobs import JobOutputSerialiser
from ...permissions import IsAuthenticated, AllowNone
from ..mixins import SoftDeleteViewSet, DownloadableViewSet
from .._UFDLBaseViewSet import UFDLBaseViewSet


class JobOutputViewSet(DownloadableViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = JobOutput.objects.all()
    serializer_class = JobOutputSerialiser

    admin_permission_class = AllowNone

    permission_classes = {
        "list": AllowNone,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "hard_delete": AllowNone,
        "reinstate": AllowNone,
        "download": IsAuthenticated
    }
