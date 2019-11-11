from rest_framework.permissions import IsAuthenticated as IsAuthenticatedOrig


class IsAuthenticated(IsAuthenticatedOrig):
    """
    Override for the built-in IsAuthenticated permission class
    which adds object support.
    """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
