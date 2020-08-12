import json

from rest_framework import serializers

from ...models.jobs import Job, JobTemplate, JobOutput
from ...models.nodes import DockerImage
from ..mixins import SoftDeleteModelSerialiser


class JobTemplateSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the template on
    which a job is based.
    """
    class Meta:
        model = JobTemplate
        fields = ["pk",
                  "name",
                  "version"]


class DockerImageSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the Docker image
    used by a job.
    """
    class Meta:
        model = DockerImage
        fields = ["pk",
                  "name",
                  "version"]


class JobOutputSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the outputs
    of a job.
    """
    class Meta:
        model = JobOutput
        fields = ["name",
                  "type"]


class JobSerialiser(SoftDeleteModelSerialiser):
    template = JobTemplateSerialiser(read_only=True)
    docker_image = DockerImageSerialiser(read_only=True)
    outputs = JobOutputSerialiser(many=True, read_only=True)

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
        read_only_fields = ["template",
                            "docker_image",
                            "start_time",
                            "end_time",
                            "error",
                            "input_values",
                            "parameter_values",
                            "node",
                            "outputs"]
