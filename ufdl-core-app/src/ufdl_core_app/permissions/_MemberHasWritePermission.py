from ._MemberPermission import MemberPermission


class MemberHasWritePermission(MemberPermission):
    """
    Checks if the member has write permission.
    """
    def check_member_permissions(self, membership, request, view, obj) -> bool:
        # Local import to avoid circular references
        from ..models import Membership

        return membership.permissions in (Membership.PERMISSION_WRITE,
                                          Membership.PERMISSION_ADMIN)
