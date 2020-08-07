from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobTemplate, JobType
from ..mixins import SoftDeleteModelSerialiser


class JobTemplateSerialiser(SoftDeleteModelSerialiser):
    # Slug fields require explicit definition
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    type = serializers.SlugRelatedField("name", queryset=JobType.objects)
    inputs = serializers.SlugRelatedField("signature", many=True, read_only=True)
    parameters = serializers.SlugRelatedField("signature", many=True, read_only=True)

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
                  "parameters"] + SoftDeleteModelSerialiser.base_fields
