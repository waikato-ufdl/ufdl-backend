from django.db.utils import IntegrityError

from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from ufdl.json.core.filter import FilterSpec

from ..exceptions import JSONParseFailure, CreateViolatesUnique
from ..filter import filter_list_request
from ..logging import get_backend_logger
from ..permissions import IsAdminUser
from ..signals import all_requests
from ..util import for_user


class UFDLBaseViewSet(ModelViewSet):
    """
    Modifies the permissions of a model view-set so that they can be defined per-action (list, create, etc.).

    Inheritors of this class should define 3 sets of permissions:
     - admin_permission_class: The class of permissions that give access to all methods.
     - permission_classes: A dictionary of action-names to permissions classes for those actions.
     - default_permissions: The class of permissions to apply to actions not found in permissions_classes.

    Automatically logs requests/responses to the database log.
    """
    # The admin permission (override access to any action)
    admin_permission_class = IsAdminUser

    # The base router only allows detail access by primary key
    lookup_value_regex = '[0-9]+'

    def get_permissions(self):
        # Permissions must be defined as a dictionary from
        # action name to permissions
        if not isinstance(self.permission_classes, dict):
            raise TypeError(f"Permission classes must be defined as a dict, "
                            f"got {type(self.permission_classes)}")

        # Get the explicitly defined permissions class or default
        permission_class = self.permission_classes.get(self.action, None)

        # If the permissions are not explicitly defined, error
        if permission_class is None:
            raise Exception(f"No permission class defined for action '{self.action}'")

        # Require either admin permissions or the defined permissions
        return [(self.admin_permission_class | permission_class)()]

    def get_queryset(self):
        query_set = super().get_queryset()

        # Use the full query-set for most actions, but list only
        # those objects that the user has permissions for.
        if self.action == "list":
            query_set = for_user(query_set, self.request.user)

            # Further filter the query-set with any filter arguments
            # supplied with the request
            filter_spec = JSONParseFailure.attempt(dict(self.request.data), FilterSpec)
            query_set = filter_list_request(query_set, filter_spec)

        return query_set

    def initial(self, request, *args, **kwargs):
        # Run the initialisation of the request as usual
        try:
            super().initial(request, *args, **kwargs)

        # If an error occurs during initialisation, log it
        except Exception as e:
            get_backend_logger().exception(self.format_request_log_message(request), exc_info=e)
            raise

        # Otherwise log the request
        get_backend_logger().info(self.format_request_log_message(request))

        all_requests.send(self.__class__, request=request)

    def format_request_log_message(self, request: Request) -> str:
        """
        Formats the automatic logging message from the request.

        :param request:     The current request.
        :return:            The logging message.
        """
        return (
            f"URI='{request.get_full_path()}'\n"
            f"METHOD='{request.method}'\n"
            f"ACTION='{self.action}'\n"
            f"DATA={request.data}\n"
            f"USER={request.user}\n"
        )

    def finalize_response(self, request, response, *args, **kwargs):
        # Log the response
        get_backend_logger().info(self.format_response_log_message(response))

        # Finalise the response as normal
        return super().finalize_response(request, response, *args, **kwargs)

    def format_response_log_message(self, response):
        """
        Formats the automatic logging message for the response.

        :param response:    The response to the current request.
        :return:            The log message for the response.
        """
        return (
            f"STATUS={response.status_code}\n"
            f"DATA={response.data if not isinstance(response.data, bytes) else '<binary data>'}"
        )

    def perform_create(self, serializer):
        try:
            super().perform_create(serializer)
        except IntegrityError as e:
            raise CreateViolatesUnique(str(e)) from e
