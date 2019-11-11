from ..models import Organisation
from ..serialisers import OrganisationSerialiser
from ..permissions import IsAuthenticated, IsMember, IsAdminUser, MemberHasAdminPermission
from ._UFDLBaseViewSet import UFDLBaseViewSet


class OrganisationViewSet(UFDLBaseViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerialiser

    admin_permission_class = IsAdminUser | MemberHasAdminPermission
    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsMember],
    }
