from typing import List

from rest_framework import routers
from rest_framework.request import Request
from rest_framework.response import Response

from simple_django_teams.models import Membership, Team

from ufdl.json.core import MembershipModSpec

from wai.json.raw import RawJSONObject

from ...exceptions import *
from ...models import User
from ...serialisers import MembershipSerialiser
from ._RoutedViewSet import RoutedViewSet


class MembershipViewSet(RoutedViewSet):
    """
    Mixin for the TeamViewSet which adds the ability to add members to
    the team.
    """
    # The keyword used to specify when the view-set is in copyable mode
    MODE_KEYWORD: str = "membership"

    @classmethod
    def get_routes(cls) -> List[routers.Route]:
        return [
            routers.Route(
                url=r'^{prefix}/{lookup}/memberships{trailing_slash}$',
                mapping={'patch': 'modify_memberships'},
                name='{basename}-memberships',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: MembershipViewSet.MODE_KEYWORD}
            ),
            routers.Route(
                url=r'^{prefix}/{lookup}/permissions/(?P<un>.*){trailing_slash}$',
                mapping={'get': 'get_permissions_for_user'},
                name='{basename}-permissions',
                detail=True,
                initkwargs={cls.MODE_ARGUMENT_NAME: MembershipViewSet.MODE_KEYWORD}
            )
        ]

    def modify_memberships(self, request: Request, pk=None):
        """
        Action to add a member to a team.

        :param request:     The request.
        :param pk:          The primary key of the team being accessed.
        :return:            The response containing the new membership record.
        """
        # Get the mod-spec from the request
        mod_spec = JSONParseFailure.attempt(dict(request.data), MembershipModSpec)

        # Get the User record for the username
        user = User.objects.filter(username=mod_spec.username).first()

        # If the user doesn't exist, error
        if user is None:
            raise BadName(mod_spec.username, "No user with this username exists")

        # If the user is deleted, error
        if not user.is_active:
            raise BadName(mod_spec.username, "This user is no longer active")

        # Get the method to use to make the modification
        if mod_spec.method == "add":
            method = self.add_membership
        elif mod_spec.method == "remove":
            method = self.remove_membership
        else:  # mod_spec.method == "update"
            method = self.update_membership

        return Response(method(self.get_object_of_type(Team), user, mod_spec.permissions, request.user))

    @staticmethod
    def add_membership(team: Team, user: User, permissions: str, modifier: User) -> RawJSONObject:
        """
        Adds a membership between the given user and team, with the given permissions.

        :param team:            The team to add the membership to.
        :param user:            The user becoming a member.
        :param permissions:     The permissions to give the user.
        :param modifier:        The user making the modification.
        :return:                The JSON representation of the membership.
        """
        # Create the membership
        membership = Membership(user=user,
                                team=team,
                                permissions=permissions,
                                creator=modifier)
        membership.save()

        return MembershipSerialiser().to_representation(membership)

    @staticmethod
    def remove_membership(team: Team, user: User, permissions: str, modifier: User) -> RawJSONObject:
        """
        Removes a membership between the given user and team.

        :param team:            The team to remove the membership from.
        :param user:            The user losing membership status.
        :param permissions:     Unused.
        :param modifier:        The user making the modification.
        :return:                The JSON representation of the membership.
        """
        # Find the membership
        membership = Membership.objects.filter(Membership.active_Q, team=team, user=user).first()

        # If there is no membership, raise an error
        if membership is None:
            raise BadName(user.username, f"This user is not a member of team {team.name}")

        # Delete the membership
        membership.delete()

        return MembershipSerialiser().to_representation(membership)

    @staticmethod
    def update_membership(team: Team, user: User, permissions: str, modifier: User) -> RawJSONObject:
        """
        Modifies the permissions of a membership.

        :param team:            The team the membership is to.
        :param user:            The user whose membership it is.
        :param permissions:     The new permissions for the user.
        :param modifier:        The user making the modification.
        :return:                The JSON representation of the membership.
        """
        # Find the membership
        membership = Membership.objects.filter(Membership.active_Q, team=team, user=user).first()

        # If there is no membership, raise an error
        if membership is None:
            raise BadName(user.username, f"This user is not a member of team {team.name}")

        # Modify the permissions of the membership
        membership.permissions = permissions
        membership.save()

        return MembershipSerialiser().to_representation(membership)

    def get_permissions_for_user(self, request: Request, pk=None, un=None):
        """
        Gets the permissions a user has with respect to this team.

        :param request:     The request.
        :param pk:          The primary key of the team being accessed.
        :param un:          The username of the user to get the permissions of.
        :return:            The response containing the new membership record.
        """
        # Get the User record for the username
        user = User.objects.filter(username=un).first()

        # If the user doesn't exist, error
        if user is None:
            raise BadName(un, "No user with this username exists")

        # Get the detailed team
        team = self.get_object_of_type(Team)

        # Find the membership
        membership = Membership.objects.filter(Membership.active_Q, team=team, user=user).first()

        # If there is no membership, raise an error
        if membership is None:
            raise BadName(user.username, f"This user is not a current member of team {team.name}")

        # Return the permissions
        return Response(membership.permissions)
