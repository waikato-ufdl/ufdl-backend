from ._MemberPermission import MemberPermission


class IsOwnMembership(MemberPermission):
    """
    Checks if the member is accessing their own membership.
    """
    def check_member_permissions(self, membership, request, view, obj) -> bool:
        return obj == membership
