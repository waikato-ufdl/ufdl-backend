from simple_django_teams.models import Membership

from ._MemberPermission import MemberPermission


class MemberHasWritePermission(MemberPermission):
    """
    Checks if the member has write permission.
    """
    permissions_set = frozenset((Membership.PERMISSION_WRITE,
                                 Membership.PERMISSION_ADMIN))

    def check_member_permissions(self, membership, request, view, obj) -> bool:
        return membership.permissions in self.permissions_set
