from rest_framework.serializers import ModelSerializer

from simple_django_teams.models import Team

from ..models import User
from .mixins import SoftDeleteModelSerialiser


class MemberSerialiser(ModelSerializer):
    """
    Specialised serialiser for serialising the members
    of a team.
    """
    class Meta:
        model = User
        fields = ["pk", "username"]


class TeamSerialiser(SoftDeleteModelSerialiser):
    members = MemberSerialiser(many=True, read_only=True, source="active_members")

    class Meta:
        model = Team
        fields = ["pk", "name", "members"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["members"]
