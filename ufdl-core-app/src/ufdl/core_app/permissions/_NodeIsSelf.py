from ..models.nodes import Node
from ._NodePermission import NodePermission


class NodeIsSelf(NodePermission):
    """
    Permission that that applies to actions on nodes that
    requires that the node is accessing itself
    """
    def has_node_permission(self, node, request, view, obj) -> bool:
        # If the object is missing, trivially pass
        # (object-specific check will fail later if appropriate)
        if obj is None:
            return True

        # Only applies to object permissions on jobs
        if not isinstance(obj, Node):
            raise TypeError(
                f"{NodeIsSelf.__name__} permission only applies to actions on nodes "
                f"(received object of type {obj.__class__.__name__})"
            )

        return obj == node
