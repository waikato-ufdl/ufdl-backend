from rest_framework import serializers
from simple_django_teams.models import Team

from .mixins import SoftDeleteModelSerialiser


class TeamSerialiser(SoftDeleteModelSerialiser):
    # Members has to be explicitly specified to use the slug
    members = serializers.SlugRelatedField("username", many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["pk", "name", "members"] + SoftDeleteModelSerialiser.base_fields
