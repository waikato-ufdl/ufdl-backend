from rest_framework import permissions


class AllowNone(permissions.BasePermission):
    """
    Permission for when access is not allowed under any circumstances.
    """
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
