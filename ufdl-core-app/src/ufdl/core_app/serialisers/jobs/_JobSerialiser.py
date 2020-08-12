import json

from rest_framework import serializers

from ...models.jobs import Job
from ..mixins import SoftDeleteModelSerialiser


class JobSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    template = serializers.SlugRelatedField("name_and_version", read_only=True)
    docker_image = serializers.SlugRelatedField("name_and_version", read_only=True)
    outputs = serializers.SlugRelatedField("signature", read_only=True, many=True)

    def to_representation(self, instance):
        # Get the representation as normal
        representation = super().to_representation(instance)

        # Convert the input/parameter values from string to JSON
        representation['input_values'] = json.loads(representation['input_values'])
        parameter_values = representation['parameter_values']
        representation['parameter_values'] = json.loads(parameter_values) if parameter_values != '' else None

        return representation

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
