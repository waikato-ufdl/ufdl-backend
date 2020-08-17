from rest_framework import serializers

from ...models import DataDomain
from ...models.jobs import JobType
from ...models.nodes import DockerImage


class DockerImageSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    tasks = serializers.SlugRelatedField("name", queryset=JobType.objects, many=True)

    class Meta:
        model = DockerImage
        fields = ["pk",
                  "name",
                  "version",
                  "url",
                  "registry_url",
                  "registry_username",
                  "registry_password",
                  "cuda_version",
                  "framework",
                  "domain",
                  "tasks",
                  "min_hardware_generation",
                  "cpu",
                  "licence"]
