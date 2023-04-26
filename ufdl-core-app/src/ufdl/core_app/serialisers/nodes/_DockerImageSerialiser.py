from rest_framework import serializers

from ...models import DataDomain
from ...models.licences import Licence
from ...models.jobs import JobContract
from ...models.nodes import DockerImage, CUDAVersion, Hardware
from ._CUDAVersionSerialiser import CUDAVersionSerialiser
from ._FrameworkSerialiser import FrameworkSerialiser
from ._HardwareSerialiser import HardwareSerialiser


class DockerImageSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    domain = serializers.SlugRelatedField("name", queryset=DataDomain.objects)
    tasks = serializers.SlugRelatedField("name", queryset=JobContract.objects, many=True)
    cuda_version = serializers.SlugRelatedField("version", queryset=CUDAVersion.objects)
    min_hardware_generation = serializers.SlugRelatedField("generation", queryset=Hardware.objects)
    licence = serializers.SlugRelatedField("name", queryset=Licence.objects)

    def to_representation(self, instance: DockerImage):
        representation = super().to_representation(instance)
        representation["cuda_version"] = CUDAVersionSerialiser().to_representation(instance.cuda_version)
        representation["framework"] = FrameworkSerialiser().to_representation(instance.framework)
        representation["domain"] = instance.domain.description
        if instance.min_hardware_generation is not None:
            representation["min_hardware_generation"] = HardwareSerialiser().to_representation(instance.min_hardware_generation)
        return representation

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
