from django.db import models

from rest_framework import serializers

from ..models import Dataset
from .mixins import TeamOwnedModelSerialiser, SoftDeleteModelSerialiser


class DatasetSerialiser(TeamOwnedModelSerialiser, SoftDeleteModelSerialiser):
    # Files has to be explicitly specified to use the slug
    domain = serializers.SlugRelatedField("description", read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['files'] = {
            file['filename']: file['handle']
            for file in instance.files.annotate(
                filename=models.F('file__name__filename'),
                handle=models.F('file__file__handle')
            ).values()
        }
        return result

    class Meta:
        model = Dataset
        fields = ["pk",
                  "name",
                  "version",
                  "previous_version",
                  "description",
                  "project",
                  "licence",
                  "is_public",
                  "domain",
                  "tags"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["files"]
        extra_kwargs = {
            "tags": {"allow_blank": True}
        }

    @classmethod
    def get_team_from_validated_data(cls, validated_data):
        return validated_data["project"].team
