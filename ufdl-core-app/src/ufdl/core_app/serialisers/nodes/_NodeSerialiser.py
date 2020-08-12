from rest_framework import serializers
from ...models.nodes import Node


class NodeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["pk",
                  "ip",
                  "driver_version",
                  "hardware_generation",
                  "gpu_mem",
                  "cpu_mem",
                  "last_seen",
                  "current_job"]
        read_only_fields = ["last_seen", "current_job"]
