from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobTemplate, JobType, Input, Parameter
from ..mixins import SoftDeleteModelSerialiser


class InputSerialiser(serializers.ModelSerializer):
    """
    Specialised serialiser for serialising the inputs to a
    job template.
    """
    class Meta:
        model = Input
        fields = ["name",
                  "type",
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
    type = serializers.SlugRelatedField("name", queryset=JobType.objects)
    inputs = InputSerialiser(many=True, read_only=True)
    parameters = ParameterSerialiser(many=True, read_only=True)

    class Meta:
        model = JobTemplate
        fields = ["pk",
                  "name",
                  "version",
                  "scope",
                  "framework",
                  "domain",
                  "type",
                  "executor_class",
                  "required_packages",
                  "body",
                  "inputs",
                  "parameters",
                  "licence"] + SoftDeleteModelSerialiser.base_fields
