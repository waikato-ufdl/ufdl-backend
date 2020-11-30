from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobTemplate, JobType, Input, Parameter, WorkableTemplate
from ..mixins import SoftDeleteModelSerialiser


class InputSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the inputs to a
    job template.
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['types'] = representation['types'].split("\n")

        return representation

    class Meta:
        model = Input
        fields = ["name",
                  "types",
                  "options",
                  "help"]


class ParameterSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the parameters to a
    job template.
    """
    class Meta:
        model = Parameter
        fields = ["name",
                  "type",
                  "default",
                  "help"]


class JobTemplateSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    inputs = InputSerialiser(many=True, read_only=True)
    parameters = ParameterSerialiser(many=True, read_only=True)

    class Meta:
        model = JobTemplate
        fields = ["pk",
                  "name",
                  "version",
                  "description",
                  "scope",
                  "domain",
                  "inputs",
                  "parameters",
                  "licence"] + SoftDeleteModelSerialiser.base_fields


class WorkableTemplateSerialiser(JobTemplateSerialiser):
    type = serializers.SlugRelatedField("name", queryset=JobType.objects)

    class Meta(JobTemplateSerialiser.Meta):
        model = WorkableTemplate
        fields = JobTemplateSerialiser.Meta.fields + [
            "framework",
            "type",
            "executor_class",
            "required_packages",
            "body"
        ]
