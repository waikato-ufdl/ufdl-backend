from rest_framework import serializers
from ...models.nodes import Framework


class FrameworkSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = ["pk",
                  "name",
                  "version"]
