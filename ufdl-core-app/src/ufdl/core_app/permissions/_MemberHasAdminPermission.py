from simple_django_teams.models import Membership

from ._MemberPermission import MemberPermission


class MemberHasAdminPermission(MemberPermission):
    """
    Checks if the member has admin permission.
    """
    def check_member_permissions(self, membership, request, view, obj) -> bool:
        return membership.permissions == Membership.PERMISSION_ADMIN
