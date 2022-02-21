import json

from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobTemplate, Parameter, WorkableTemplate, MetaTemplate
from ..mixins import SoftDeleteModelSerialiser


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

    def to_representation(self, instance: JobTemplate):
        representation = super().to_representation(instance)

        instance = instance.upcast()

        if isinstance(instance, WorkableTemplate):
            instance: WorkableTemplate
            representation["type"] = instance.type
            representation["executor_class"] = instance.executor_class
            representation["required_packages"] = instance.required_packages

            parameters = {}
            for parameter in instance.parameters.all():
                parameter_json = {
                    "types": parameter.types.split("|"),
                    "help": parameter.help
                }
                if parameter.default is not None:
                    parameter_json.update({
                        "default": json.loads(parameter.default),
                        "default_type": parameter.default_type,
                        "const": parameter.const
                    })
                parameters[parameter.name] = parameter_json
            representation["parameters"] = parameters
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
                  "licence"] + SoftDeleteModelSerialiser.base_fields
