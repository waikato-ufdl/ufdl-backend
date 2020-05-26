from ..models.licences import Licence
from ..serialisers import LicenceSerialiser
from ..permissions import IsAdminUser, IsAuthenticated
from .mixins import LicenceSubdescriptorViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class LicenceViewSet(LicenceSubdescriptorViewSet, UFDLBaseViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerialiser

    admin_permission_class = IsAdminUser
    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
