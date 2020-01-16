from simple_django_teams.models import Team

from ..serialisers import TeamSerialiser
from ..permissions import IsAuthenticated, IsMember, IsAdminUser, MemberHasAdminPermission
from .mixins import MembershipViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class TeamViewSet(MembershipViewSet, UFDLBaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerialiser

    admin_permission_class = IsAdminUser | MemberHasAdminPermission
    default_permissions = []

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsMember],
    }
