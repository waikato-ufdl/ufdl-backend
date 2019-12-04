from simple_django_teams.models import Team

from ._SoftDeleteModelSerialiser import SoftDeleteModelSerialiser


class TeamSerialiser(SoftDeleteModelSerialiser):
    class Meta:
        model = Team
        fields = ["name"] + SoftDeleteModelSerialiser.base_fields
