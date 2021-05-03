from simple_django_teams.models import Team

from ..serialisers import TeamSerialiser
from ..permissions import IsAuthenticated, IsMember, MemberHasAdminPermission, AllowNone
from .mixins import MembershipViewSet, SoftDeleteViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class TeamViewSet(MembershipViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerialiser

    permission_classes = {
        "list": IsAuthenticated,
        "create": AllowNone,
        "retrieve": IsMember,
        "update": MemberHasAdminPermission,
        "partial_update": MemberHasAdminPermission,
        "destroy": MemberHasAdminPermission,
        "modify_memberships": MemberHasAdminPermission,
        "get_permissions_for_user": MemberHasAdminPermission,
        "hard_delete": AllowNone,
        "reinstate": AllowNone
    }
