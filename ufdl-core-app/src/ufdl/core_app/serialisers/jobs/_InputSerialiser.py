from rest_framework import serializers

from ...models.jobs import Input


class InputSerialiser(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['types'] = representation['types'].split("\n")

    class Meta:
        model = Input
        fields = ["pk",
                  "name",
                  "types",
                  "options",
                  "help"]
