from ._MemberPermission import MemberPermission


class MemberHasAdminPermission(MemberPermission):
    """
    Checks if the member has admin permission.
    """
    def has_object_permission(self, request, view, obj):
        print("HERE")
        return super().has_object_permission(request, view, obj)

    def check_member_permissions(self, membership, request, view, obj) -> bool:
        # Local import to avoid circular references
        from ..models import Membership

        print(membership.permissions)

        return membership.permissions == Membership.PERMISSION_ADMIN
