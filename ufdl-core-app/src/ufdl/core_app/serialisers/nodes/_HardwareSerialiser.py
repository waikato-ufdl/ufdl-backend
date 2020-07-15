from rest_framework import serializers
from ...models.nodes import Hardware


class HardwareSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = ["pk",
                  "generation",
                  "compute_capability"]
