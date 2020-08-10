from typing import Optional

from rest_framework.permissions import BasePermission

from ..models import User


class NodePermission(BasePermission):
    """
    Base class for permissions of worker nodes.
    """
    def has_permission(self, request, view):
        # Get the user
        user = self._get_node_from_request(request)

        # If the user is not an active node, permission denied
        if user is None:
            return False

        return self.has_node_permission(user, request, view, None)

    def has_object_permission(self, request, view, obj):
        # Get the user
        user = self._get_node_from_request(request)

        # If the user is not an active node, permission denied
        if user is None:
            return False

        return self.has_node_permission(user, request, view, obj)

    def has_node_permission(self, node, request, view, obj) -> bool:
        """
        Checks if the user is allowed to perform the action they are trying
        to perform.

        :param node:        The node user.
        :param request:     The request.
        :param view:        The view.
        :param obj:         Optionally the object being operated on.
        """
        raise NotImplementedError(NodePermission.has_node_permission.__qualname__)

    def _get_node_from_request(self, request) -> Optional[User]:
        """
        Gets the node user from the request, if it is one.

        :param request:     The request.
        :return:            The user, or None if the user is not a node.
        """
        # Get the user
        user = request.user

        # Make sure it is an active node
        if not isinstance(user, User) or not user.is_node or not user.is_active:
            return None

        return user
