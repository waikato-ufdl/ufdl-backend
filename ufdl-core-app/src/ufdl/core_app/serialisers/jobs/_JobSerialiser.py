from rest_framework import serializers

from ...models.jobs import Job
from ..mixins import SoftDeleteModelSerialiser


class JobSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    template = serializers.SlugRelatedField("name_and_version", read_only=True)
    docker_image = serializers.SlugRelatedField("name_and_version", read_only=True)
    outputs = serializers.SlugRelatedField("signature", read_only=True, many=True)

    class Meta:
        model = Job
        fields = ["pk",
                  "template",
                  "docker_image",
                  "start_time",
                  "end_time",
                  "error",
                  "input_values",
                  "parameter_values",
                  "node",
                  "outputs"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["start_time",
                            "end_time",
                            "error",
                            "input_values",
                            "parameter_values",
                            "node",
                            "outputs"]
