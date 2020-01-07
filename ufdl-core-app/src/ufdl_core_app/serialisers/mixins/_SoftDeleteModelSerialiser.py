from rest_framework import serializers


class SoftDeleteModelSerialiser(serializers.ModelSerializer):
    """
    Base class for common functionality of serialisers.
    """
    # The fields covered by the base serialiser
    base_fields = ["creator", "creation_time", "deletion_time"]

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)
