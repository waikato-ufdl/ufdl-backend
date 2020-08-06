from simple_django_teams.models import Team

from ..serialisers import TeamSerialiser
from ..permissions import IsAuthenticated, IsMember, IsAdminUser, MemberHasAdminPermission
from .mixins import MembershipViewSet, SoftDeleteViewSet
from ._UFDLBaseViewSet import UFDLBaseViewSet


class TeamViewSet(MembershipViewSet, SoftDeleteViewSet, UFDLBaseViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerialiser

    admin_permission_class = IsAdminUser | MemberHasAdminPermission

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsMember],
    }
