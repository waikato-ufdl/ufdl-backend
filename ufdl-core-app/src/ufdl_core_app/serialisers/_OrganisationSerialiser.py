from rest_framework import serializers

from ..models import Organisation


class OrganisationSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["name", "creation_time", "creator", "deletion_time"]

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
