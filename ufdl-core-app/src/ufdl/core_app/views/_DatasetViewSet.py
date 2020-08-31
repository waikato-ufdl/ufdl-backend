from rest_framework.permissions import AllowAny

from ..models import Dataset
from ..serialisers import DatasetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublic, AllowNone
from .mixins import DownloadableViewSet, CopyableViewSet, FileContainerViewSet, SoftDeleteViewSet, MergeViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DatasetViewSet(MergeViewSet, DownloadableViewSet, CopyableViewSet, FileContainerViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = {
        "list": AllowAny,
        "create": MemberHasWritePermission,
        "retrieve": IsMember | IsPublic,
        "update": MemberHasWritePermission,
        "partial_update": MemberHasWritePermission,
        "destroy": MemberHasWritePermission,
        "merge": MemberHasWritePermission,
        "download": IsMember,
        "copy": IsMember,
        "add_file": MemberHasWritePermission,
        "get_file": IsMember,
        "delete_file": MemberHasWritePermission,
        "set_metadata": MemberHasWritePermission,
        "get_metadata": IsMember,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }
