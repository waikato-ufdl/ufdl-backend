from rest_framework import serializers

from ...models.jobs import Input


class InputSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ["pk",
                  "name",
                  "type",
                  "options",
                  "help"]
