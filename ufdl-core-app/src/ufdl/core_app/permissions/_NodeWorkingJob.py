from ..models import Job
from ._NodePermission import NodePermission


class NodeWorkingJob(NodePermission):
    """
    Permission that that applies to actions on jobs that
    requires that the node thinks it is working the job.
    """
    def has_node_permission(self, node, request, view, obj) -> bool:
        # If the object is missing, trivially pass
        # (object-specific check will fail later if appropriate)
        if obj is None:
            return True

        # Only applies to object permissions on jobs
        if not isinstance(obj, Job):
            raise TypeError(
                f"{NodeWorkingJob.__name__} permission only applies to actions on jobs "
                f"(received object of type {obj.__class__.__name__})"
            )

        return node.current_job == obj
