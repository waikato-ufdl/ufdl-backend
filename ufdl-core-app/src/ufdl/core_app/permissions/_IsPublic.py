from rest_framework import permissions
from simple_django_teams.util import ensure_model


class IsPublic(permissions.BasePermission):
    """
    Permission for when the object being handled is a public object.
    """
    def has_object_permission(self, request, view, obj):
        # Local imports to avoid circular references
        from ..mixins import PublicModel

        # Make sure the object is a dataset
        ensure_model(obj, PublicModel)

        return obj.is_public
