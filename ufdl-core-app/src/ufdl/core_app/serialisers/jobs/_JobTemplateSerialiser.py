from rest_framework import serializers

from ...models import DataDomain
from ...models.nodes import Framework
from ...models.jobs import JobTemplate, JobType, Input, Parameter
from ..mixins import SoftDeleteModelSerialiser


class JobTemplateSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    framework = serializers.SlugRelatedField("name_and_version", queryset=Framework.objects)
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    type = serializers.SlugRelatedField("name", queryset=JobType.objects)
    inputs = serializers.SlugRelatedField("signature", queryset=Input.objects, many=True, read_only=True)
    parameters = serializers.SlugRelatedField("signature", queryset=Parameter.objects, many=True, read_only=True)


    class Meta:
        model = JobTemplate
        fields = ["pk",
                  "name",
                  "version",
                  "scope",
                  "executor_class",
                  "required_packages",
                  "body"] + SoftDeleteModelSerialiser.base_fields
