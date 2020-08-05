from rest_framework import serializers

from ...models.nodes import DockerImage
from ...models.jobs import JobTemplate, Job
from ..mixins import SoftDeleteModelSerialiser


class JobSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    template = serializers.SlugRelatedField("name_and_version", queryset=JobTemplate.objects.active())
    docker_image = serializers.SlugRelatedField("name_and_version", queryset=DockerImage.objects)

    class Meta:
        model = Job
        fields = ["pk",
                  "start_time",
                  "end_time",
                  "error",
                  "input_values",
                  "parameter_values",
                  "node",
                  "outputs"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["error",
                            "input_values",
                            "parameter_values",
                            "node",
                            "outputs"]
