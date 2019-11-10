from rest_framework.permissions import IsAdminUser, AllowAny

from ..models import Dataset
from ..serialisers import DatasetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublicDataset
from ._PerActionPermissionsModelViewSet import PerActionPermissionsModelViewSet


class DatasetViewSet(PerActionPermissionsModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission

    permission_classes = {
        "list": [AllowAny],  # List filtering is done seperately
        "retrieve": [IsMember | IsPublicDataset]
    }
