from ._MemberPermission import MemberPermission


class IsMember(MemberPermission):
    """
    Checks if the member has admin permission.
    """
    def check_member_permissions(self, membership, request, view, obj) -> bool:
        return True
