from rest_framework.permissions import AllowAny

from ..models import DataAsset
from ..serialisers import DataAssetSerialiser
from ..permissions import IsAdminUser
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DataAssetViewSet(UFDLBaseViewSet):
    queryset = DataAsset.objects.all()
    serializer_class = DataAssetSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [AllowAny]  # List filtering is done seperately
    }
