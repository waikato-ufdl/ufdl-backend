from rest_framework import serializers
from ...models.nodes import Hardware


class HardwareSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        fields = ["pk",
                  "generation",
                  "min_compute_capability",
                  "max_compute_capability"]
