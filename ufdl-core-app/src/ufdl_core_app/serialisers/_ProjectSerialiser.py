from ..models import Project
from ._TeamOwnedModelSerialiser import TeamOwnedModelSerialiser
from ._SoftDeleteModelSerialiser import SoftDeleteModelSerialiser


class ProjectSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    class Meta:
        model = Project
        fields = ["id",
                  "name",
                  "team"] + SoftDeleteModelSerialiser.base_fields

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["team"]
