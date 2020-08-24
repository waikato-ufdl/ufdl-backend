from rest_framework.permissions import BasePermission

from ..models.nodes import Node


class NodePermission(BasePermission):
    """
    Base class for permissions of worker nodes.
    """
    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)

    def has_object_permission(self, request, view, obj):
        # Get the node
        node = Node.from_request(request)

        # If a node is not specified, permission denied
        if node is None:
            return False

        return self.has_node_permission(node, request, view, obj)

    def has_node_permission(self, node, request, view, obj) -> bool:
        """
        Checks if the user is allowed to perform the action they are trying
        to perform.

        :param node:        The node.
        :param request:     The request.
        :param view:        The view.
        :param obj:         Optionally the object being operated on.
        """
        raise NotImplementedError(NodePermission.has_node_permission.__qualname__)
