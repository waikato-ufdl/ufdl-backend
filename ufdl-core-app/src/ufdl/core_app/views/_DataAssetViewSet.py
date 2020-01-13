from rest_framework.permissions import AllowAny

from ..models import DataAsset
from ..serialisers import DataAssetSerialiser
from ..permissions import IsAdminUser
from .mixins import AsFileViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DataAssetViewSet(AsFileViewSet, UFDLBaseViewSet):
    queryset = DataAsset.objects.all()
    serializer_class = DataAssetSerialiser

    admin_permission_class = IsAdminUser

    permission_classes = {
        "list": [AllowAny]  # List filtering is done seperately
    }
