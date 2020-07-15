from rest_framework import serializers
from ...models.nodes import CUDAVersion


class CUDAVersionSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CUDAVersion
        fields = ["pk",
                  "version",
                  "full_version",
                  "min_driver_version"]
