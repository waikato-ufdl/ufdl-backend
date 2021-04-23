from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobTemplate, Input, Parameter, WorkableTemplate, MetaTemplate
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

    def to_representation(self, instance: JobTemplate):
        representation = super().to_representation(instance)

        instance = instance.upcast()

        if isinstance(instance, WorkableTemplate):
            instance: WorkableTemplate
            representation["framework"] = instance.framework.pk
            representation["type"] = instance.type.name
            representation["executor_class"] = instance.executor_class
            representation["required_packages"] = instance.required_packages
            representation["body"] = instance.body
        else:
            instance: MetaTemplate
            pass  # Currently not adding any additional information for meta-templates

        return representation

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
