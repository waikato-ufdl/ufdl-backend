from ._MemberPermission import MemberPermission


class MemberHasAdminPermission(MemberPermission):
    """
    Checks if the member has admin permission.
    """
    def check_member_permissions(self, membership, request, view, obj) -> bool:
        # Local import to avoid circular references
        from ..models import Membership

        return membership.permissions == Membership.PERMISSION_ADMIN
