from simple_django_teams.models import Membership

from .mixins import TeamOwnedModelSerialiser, SoftDeleteModelSerialiser


class MembershipSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    class Meta:
        model = Membership
        fields = ["user",
                  "team",
                  "permissions"] + SoftDeleteModelSerialiser.base_fields

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["team"]
