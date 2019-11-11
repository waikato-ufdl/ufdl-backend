from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from ..permissions import IsAdminUser


class UFDLBaseViewSet(ModelViewSet):
    """
    Modifies the permissions of a model view-set so that
    they can be defined per-action (list, create, etc.).
    """
    # The permissions to use when an action isn't listed in the permission_classes dictionary
    default_permissions = [~AllowAny]

    # The admin permission (override access to any action)
    admin_permission_class = IsAdminUser

    def get_permissions(self):
        # If permissions defined as a list, just act normally
        if isinstance(self.permission_classes, list):
            return super().get_permissions()

        # If defined as a dict from action to permissions, apply the
        # correct permissions for the current action
        if isinstance(self.permission_classes, dict):
            permission_classes = (self.permission_classes[self.action]
                                  if self.action in self.permission_classes
                                  else self.default_permissions)

            # If no permissions defined, require admin permissions
            if len(permission_classes) == 0:
                return [self.admin_permission_class()]

            return [(self.admin_permission_class | permission)()
                    for permission in permission_classes]

        raise TypeError(f"Permission classes must be defined as a list or dict, "
                        f"got {type(self.permission_classes)}")

    def get_queryset(self):
        query_set = super().get_queryset()

        # Use the full query-set for most actions, but list can't only
        # those objects that the user has permissions for.
        if self.action == "list":
            query_set = query_set.for_user(self.request.user)

        return query_set
