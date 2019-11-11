from rest_framework.permissions import AllowAny

from ..models import Dataset
from ..serialisers import DatasetSerialiser
from ..permissions import MemberHasWritePermission, IsMember, IsPublicDataset, IsAdminUser
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DatasetViewSet(UFDLBaseViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerialiser

    admin_permission_class = IsAdminUser | MemberHasWritePermission

    permission_classes = {
        "list": [AllowAny],  # List filtering is done seperately
        "retrieve": [IsMember | IsPublicDataset]
    }
