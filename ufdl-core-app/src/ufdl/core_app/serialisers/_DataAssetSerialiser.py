from ..models import DataAsset
from .mixins import TeamOwnedModelSerialiser


class DataAssetSerialiser(TeamOwnedModelSerialiser):
    class Meta:
        model = DataAsset
        fields = ["filename",
                  "dataset"]

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["dataset"].project.team
