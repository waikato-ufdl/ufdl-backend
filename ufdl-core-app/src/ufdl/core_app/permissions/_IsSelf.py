from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    """
    Permission for user's accessing their own user information.
    """
    def has_permission(self, request, view):
        return view.action == "get_by_name" and request.user.username == view.kwargs['name']

    def has_object_permission(self, request, view, obj):
        return view.action == "retrieve" and obj == request.user
