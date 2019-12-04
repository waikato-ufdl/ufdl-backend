from simple_django_teams.models import Membership

from ..serialisers import MembershipSerialiser
from ..permissions import MemberHasAdminPermission, IsAuthenticated, IsAdminUser, IsOwnMembership
from ._UFDLBaseViewSet import UFDLBaseViewSet


class MembershipViewSet(UFDLBaseViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerialiser

    admin_permission_class = IsAdminUser | MemberHasAdminPermission
    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsOwnMembership]
    }
