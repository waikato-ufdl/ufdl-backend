from ._NodePermission import NodePermission


class IsNode(NodePermission):
    """
    Permission requiring that the user is a worker node.
    """
    def has_node_permission(self, node, request, view, obj) -> bool:
        return True
