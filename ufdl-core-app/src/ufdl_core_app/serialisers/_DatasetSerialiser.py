from ..models import Dataset
from ._TeamOwnedModelSerialiser import TeamOwnedModelSerialiser
from ._SoftDeleteModelSerialiser import SoftDeleteModelSerialiser


class DatasetSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    class Meta:
        model = Dataset
        fields = ["name",
                  "version",
                  "project",
                  "licence",
                  "is_public",
                  "tags"] + SoftDeleteModelSerialiser.base_fields
        extra_kwargs = {
            "tags": {"allow_blank": True}
        }

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["project"].team
