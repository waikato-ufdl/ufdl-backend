from rest_framework import serializers
from ...models.nodes import DockerImage, CUDAVersion, Hardware


class DockerImageSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    cuda_version = serializers.SlugRelatedField("full_version", queryset=CUDAVersion.objects)
    min_hardware_generation = serializers.SlugRelatedField("generation", queryset=Hardware.objects)

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
                  "framework_version",
                  "domain",
                  "task",
                  "min_hardware_generation"]
