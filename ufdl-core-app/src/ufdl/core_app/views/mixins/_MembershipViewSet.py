from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from simple_django_teams.models import Membership

from ...exceptions import *
from ...models import User
from ...serialisers import MembershipSerialiser
from ._RoutedViewSet import RoutedViewSet

# Translates the possible values for the permissions parameter into the
# form expected by the membership model
PERMISSIONS_TRANSLATION_TABLE = {
    "READ": Membership.PERMISSION_READ,
    "R": Membership.PERMISSION_READ,
    "WRITE": Membership.PERMISSION_WRITE,
    "W": Membership.PERMISSION_WRITE,
    "ADMIN": Membership.PERMISSION_ADMIN,
    "A": Membership.PERMISSION_ADMIN
}


class MembershipViewSet(RoutedViewSet):
    """
    Mixin for the TeamViewSet which adds the ability to add members to
    the team.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "membership"

    @classmethod
    def get_route(cls) -> routers.Route:
        return routers.Route(
            url=r'^{prefix}/{lookup}/add-member{trailing_slash}$',
            mapping={'post': 'add_member'},
            name='{basename}-add-member',
            detail=True,
            initkwargs={cls.MODE_ARGUMENT_NAME: MembershipViewSet.MODE_KEYWORD}
        )

    def add_member(self, request: Request, pk=None):
        """
        Action to add a member to a team.

        :param request:     The request.
        :param pk:          The primary key of the team being accessed.
        :return:            The response containing the new membership record.
        """
        # Get the parameters from the request
        parameters = dict(request.data)

        # Make sure the username argument was supplied
        if "username" not in parameters:
            raise MissingParameter("username")

        # Extract the parameter values
        username = parameters.pop("username")
        permissions = parameters.pop("permissions", Membership.PERMISSION_READ)  # Default to read-only permission

        # Make sure no other parameters are provided
        if len(parameters) > 0:
            raise UnknownParameters(parameters)

        # Make sure the permissions argument is a string
        if not isinstance(permissions, str):
            raise BadArgumentType("add-member",
                                  "permissions",
                                  "string",
                                  f"{type(permissions).__name__}")

        # Make the case insensitive
        permissions = permissions.upper()

        # Make sure the permissions argument is one of the allowed values
        if permissions not in PERMISSIONS_TRANSLATION_TABLE:
            raise BadArgumentValue("add-member",
                                   "permissions",
                                   permissions,
                                   ", ".join(PERMISSIONS_TRANSLATION_TABLE.keys()))

        # Get the User record for the username
        user = User.objects.filter(username=username).first()

        # If the user doesn't exist, error
        if user is None:
            raise BadName(username, "No user with this username exists")

        # If the user is deleted, error
        if not user.is_active:
            raise BadName(username, "This user is no longer active")

        # Add the user to the team
        membership = Membership(user=user,
                                team=self.get_object(),
                                permissions=permissions,
                                creator=request.user)
        membership.save()

        return Response(MembershipSerialiser().to_representation(membership))
