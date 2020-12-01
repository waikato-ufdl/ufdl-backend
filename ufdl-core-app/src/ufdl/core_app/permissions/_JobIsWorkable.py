from rest_framework.permissions import BasePermission

from ..models.jobs import Job


class JobIsWorkable(BasePermission):
    """
    Permission requiring the job is not a meta-job.
    """
    def has_object_permission(self, request, view, obj):
        assert isinstance(obj, Job), "JobIsWorkable permission only applies to Job detail methods"

        return not obj.is_meta
