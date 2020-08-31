from ..models.licences import Licence
from ..serialisers import LicenceSerialiser
from ..permissions import IsAuthenticated, AllowNone
from .mixins import LicenceSubdescriptorViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class LicenceViewSet(LicenceSubdescriptorViewSet, UFDLBaseViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsAuthenticated,
        "update": AllowNone,
        "partial_update": AllowNone,
        "destroy": AllowNone,
        "modify_subdescriptors": AllowNone
    }
