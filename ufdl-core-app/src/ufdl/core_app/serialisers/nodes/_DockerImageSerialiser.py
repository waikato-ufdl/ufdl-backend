from rest_framework import serializers

from ...models import DataDomain
from ...models.licences import Licence
from ...models.jobs import JobType
from ...models.nodes import DockerImage
from ._CUDAVersionSerialiser import CUDAVersionSerialiser
from ._FrameworkSerialiser import FrameworkSerialiser
from ._HardwareSerialiser import HardwareSerialiser


class DockerImageSerialiser(serializers.ModelSerializer):
    # Slug fields require explicit definition
    domain = serializers.SlugRelatedField("description", queryset=DataDomain.objects)
    tasks = serializers.SlugRelatedField("name", queryset=JobType.objects, many=True)
    cuda_version = CUDAVersionSerialiser()
    framework = FrameworkSerialiser()
    min_hardware_generation = HardwareSerialiser()
    licence = serializers.SlugRelatedField("name", queryset=Licence.objects)

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
