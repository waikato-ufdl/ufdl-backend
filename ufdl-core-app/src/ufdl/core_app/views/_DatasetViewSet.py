from rest_framework.permissions import AllowAny

from ..models import Dataset
from ..serialisers import DatasetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublic, IsAdminUser
from .mixins import DownloadableViewSet, CopyableViewSet, FileContainerViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DatasetViewSet(DownloadableViewSet, CopyableViewSet, FileContainerViewSet, UFDLBaseViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission

    permission_classes = {
        "list": [AllowAny],  # List filtering is done seperately
        "retrieve": [IsMember | IsPublic],
        "as_file": [AllowAny],  # TODO: Change to a proper level of authorisation
        "add_file": [AllowAny],  # TODO: Change to a proper level of authorisation
        "get_file": [AllowAny],  # TODO: Change to a proper level of authorisation
        "delete_file": [AllowAny],  # TODO: Change to a proper level of authorisation
        "set_metadata": [AllowAny],  # TODO: Change to a proper level of authorisation
        "get_metadata": [AllowAny],  # TODO: Change to a proper level of authorisation
        "copy": [AllowAny],  # TODO: Change to a proper level of authorisation
    }
