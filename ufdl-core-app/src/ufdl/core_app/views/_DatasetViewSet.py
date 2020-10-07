from rest_framework.permissions import AllowAny

from ..models import Dataset
from ..serialisers import DatasetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublic, AllowNone, WriteOrNodeExecutePermission
from .mixins import *
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DatasetViewSet(
    ClearDatasetViewSet,
    MergeViewSet,
    DownloadableViewSet,
    CopyableViewSet,
    FileContainerViewSet,
    SoftDeleteViewSet,
    UFDLBaseViewSet
):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    permission_classes = {
        "list": AllowAny,
        "create": MemberHasWritePermission,
        "retrieve": IsMember | IsPublic,
        "update": WriteOrNodeExecutePermission,
        "partial_update": WriteOrNodeExecutePermission,
        "destroy": MemberHasWritePermission,
        "clear_dataset": WriteOrNodeExecutePermission,
        "merge": WriteOrNodeExecutePermission,
        "download": IsMember,
        "copy": IsMember,
        "add_file": WriteOrNodeExecutePermission,
        "get_file": IsMember,
        "delete_file": WriteOrNodeExecutePermission,
        "set_metadata": WriteOrNodeExecutePermission,
        "get_metadata": IsMember,
        "get_all_metadata": IsMember,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }

    def get_object_from_url(self, **kwargs):
        # Get the object as normal
        obj = super().get_object_from_url(**kwargs)

        # If it is a data-set, up-cast it automatically
        if isinstance(obj, Dataset):
            obj = obj.domain_specific

        return obj
