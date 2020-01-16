from ..models import Project
from .mixins import TeamOwnedModelSerialiser, SoftDeleteModelSerialiser


class ProjectSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    class Meta:
        model = Project
        fields = ["pk",
                  "name",
                  "team"] + SoftDeleteModelSerialiser.base_fields

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["team"]
