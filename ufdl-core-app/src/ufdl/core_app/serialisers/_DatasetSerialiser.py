from rest_framework import serializers

from ..models import Dataset
from .mixins import TeamOwnedModelSerialiser, SoftDeleteModelSerialiser


class DatasetSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    # Files has to be explicitly specified to use the slug
    files = serializers.SlugRelatedField("filename", many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ["pk",
                  "name",
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
