from rest_framework import serializers
from ...models import DataDomain
from ...models.nodes import DockerImage, CUDAVersion, Hardware


class DockerImageSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    cuda_version = serializers.SlugRelatedField("version", queryset=CUDAVersion.objects)
    min_hardware_generation = serializers.SlugRelatedField("generation", queryset=Hardware.objects, allow_null=True)
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)

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
                  "task",
                  "min_hardware_generation",
                  "cpu"]
