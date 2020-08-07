from rest_framework import serializers
from ...models.nodes import Node, Hardware


class NodeSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    hardware_generation = serializers.SlugRelatedField("generation", queryset=Hardware.objects, allow_null=True)

    class Meta:
        model = Node
        fields = ["pk",
                  "ip",
                  "driver_version",
                  "gpu_mem",
                  "cpu_mem",
                  "last_seen",
                  "current_job"]
        read_only_fields = ["last_seen", "current_job"]
