import json

from rest_framework import serializers

from ...models.jobs import Job, JobTemplate, JobOutput
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


class JobOutputSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the outputs
    of a job.
    """
    class Meta:
        model = JobOutput
        fields = [
            "pk",
            "name",
            "type"
        ]


class JobSerialiser(SoftDeleteModelSerialiser):
    template = JobTemplateSerialiser(read_only=True)
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
                  "parent",
                  "start_time",
                  "end_time",
                  "error",
                  "input_values",
                  "parameter_values",
                  "node",
                  "outputs",
                  "description"] + SoftDeleteModelSerialiser.base_fields
        read_only_fields = ["template",
                            "parent",
                            "start_time",
                            "end_time",
                            "error",
                            "input_values",
                            "parameter_values",
                            "node",
                            "outputs"]
