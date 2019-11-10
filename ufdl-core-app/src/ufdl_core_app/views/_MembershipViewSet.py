from rest_framework.permissions import IsAuthenticated

from ..models import Membership
from ..serialisers import MembershipSerialiser
from ..permissions import MemberHasAdminPermission, IsMember
from ._PerActionPermissionsModelViewSet import PerActionPermissionsModelViewSet


class MembershipViewSet(PerActionPermissionsModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerialiser

    default_permissions = [MemberHasAdminPermission]

    permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsMember]
    }
