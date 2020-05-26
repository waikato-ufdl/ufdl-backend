from rest_framework import serializers
from ..models.licences import Licence


class LicenceSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    permissions = serializers.SlugRelatedField("name", many=True, read_only=True)
    conditions = serializers.SlugRelatedField("name", many=True, read_only=True)
    limitations = serializers.SlugRelatedField("name", many=True, read_only=True)

    class Meta:
        model = Licence
        fields = ["pk",
                  "name",
                  "url",
                  "permissions",
                  "conditions",
                  "limitations"]
