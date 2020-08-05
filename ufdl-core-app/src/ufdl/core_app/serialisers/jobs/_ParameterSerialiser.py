from rest_framework import serializers

from ...models.jobs import Parameter


class ParameterSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ["pk",
                  "name",
                  "type",
                  "default"]
