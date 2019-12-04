from rest_framework import permissions
from simple_django_teams.util import ensure_model


class IsPublicDataset(permissions.BasePermission):
    """
    Permission for when the object being handled is a public dataset.
    """
    def has_object_permission(self, request, view, obj):
        # Local imports to avoid circular references
        from ..models import Dataset

        # Make sure the object is a dataset
        ensure_model(obj, Dataset)

        return obj.is_public
