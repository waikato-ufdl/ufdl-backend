from rest_framework import permissions


class IsPublicDataset(permissions.BasePermission):
    """
    Permission for when the object being handled is a public dataset.
    """
    def has_object_permission(self, request, view, obj):
        # Local imports to avoid circular references
        from ..models import Dataset

        # Make sure the object is a dataset
        if not isinstance(obj, Dataset):
            return False

        return obj.is_public
