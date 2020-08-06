from ..models import DataDomain
from ..serialisers import DataDomainSerialiser
from ..permissions import AllowNone, IsAuthenticated
from ._UFDLBaseViewSet import UFDLBaseViewSet


class DataDomainViewSet(UFDLBaseViewSet):
    queryset = DataDomain.objects.all()
    serializer_class = DataDomainSerialiser

    admin_permission_class = AllowNone  # Access to mutating methods is denied even to admins

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated]
    }
