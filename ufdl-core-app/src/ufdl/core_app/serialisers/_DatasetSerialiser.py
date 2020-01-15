from ..models import Dataset
from .mixins import TeamOwnedModelSerialiser, SoftDeleteModelSerialiser


class DatasetSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    class Meta:
        model = Dataset
        fields = ["name",
                  "version",
                  "project",
                  "licence",
                  "is_public",
                  "files",
                  "tags"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["files"]
        extra_kwargs = {
            "tags": {"allow_blank": True}
        }

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["project"].team
