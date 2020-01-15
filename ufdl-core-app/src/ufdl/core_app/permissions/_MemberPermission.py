from rest_framework import permissions
from simple_django_teams.mixins import TeamOwnedModel
from simple_django_teams.models import Membership
from simple_django_teams.util import active_membership


class MemberPermission(permissions.BasePermission):
    """
    Base class for member permissions. Checks that the user
    is a member of the relevant team before deferring
    the remainder of the permission check.
    """
    def has_permission(self, request, view):
        # Local imports to avoid circularity errors
        from ..serialisers.mixins import TeamOwnedModelSerialiser

        # List action performs it's authorisation separately,
        # and all other actions use the object permissions
        if view.action != "create":
            return True

        # Get the serialiser type for the view
        serialiser_class = view.serializer_class

        # If the team can't be inferred from the serialiser class,
        # trivially pass and we'll further discriminate later
        if not issubclass(serialiser_class, TeamOwnedModelSerialiser):
            return True

        # Create a serialiser instance for the request data
        serialiser = serialiser_class(data=request.data)

        # If the serialiser is invalid, pass the authorisation check, as
        # the call will fail on implementation anyway, and the weird form
        # test will pass.
        if not serialiser.is_valid():
            return True

        # User the instance to infer the membership to test for authorisation
        membership = serialiser.active_membership_for(request.user)

        # If the user is not a member of the team, permission denied
        if not isinstance(membership, Membership):
            return False

        return self.check_member_permissions(membership, request, view, None)

    def has_object_permission(self, request, view, obj):
        # Local imports to avoid circularity errors
        from ..models import User

        # The object being tested should imply the team it belongs to
        if not isinstance(obj, TeamOwnedModel):
            return False

        # User must be logged in
        if not isinstance(request.user, User):
            return False

        # Get the user's membership
        membership = active_membership(request.user, obj.get_owning_team())

        # If the user is not a member of the team, permission denied
        if not isinstance(membership, Membership):
            return False

        return self.check_member_permissions(membership, request, view, obj)

    def check_member_permissions(self, membership, request, view, obj) -> bool:
        """
        Checks if the user is allowed to perform the action they are trying
        to perform.

        :param membership:  The user's membership.
        :param request:     The request.
        :param view:        The view.
        :param obj:         Optionally the object being operated on.
        """
        raise NotImplementedError(MemberPermission.check_member_permissions.__qualname__)
