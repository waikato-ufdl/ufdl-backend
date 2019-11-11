from rest_framework.permissions import IsAdminUser as IsAdminUserOrig


class IsAdminUser(IsAdminUserOrig):
    """
    Override for the built-in IsAdminUser permission class
    which adds object support.
    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
