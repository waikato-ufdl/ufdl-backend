from rest_framework import serializers
from simple_django_teams.util import active_membership


class TeamOwnedModelSerialiser(serializers.ModelSerializer):
    """
    Mixin class for serialisers that can extract a team
    from their data payload.
    """
    def get_team(self):
        """
        Gets the inferred team from this serialiser's payload.

        :return:    The team.
        """
        # Make sure we're valid
        self.is_valid(raise_exception=True)

        # Get the team from the validated data
        return self.get_team_from_validated_data(self.validated_data)

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        """
        Gets the team from the validated data of the serialiser.

        :param validated_data:  The validated data.
        :return:                The team.
        """
        raise NotImplementedError(TeamOwnedModelSerialiser.get_team_from_validated_data.__qualname__)

    def active_membership_for(self, user):
        """
        Gets the active membership for the given user, relative to
        the team that owns the serialised model.

        :param user:    The user.
        :return:        The membership, or None if none available.
        """
        return active_membership(user, self.get_team())
