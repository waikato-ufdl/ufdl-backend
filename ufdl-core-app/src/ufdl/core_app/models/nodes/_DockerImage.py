from django.db import models

from ...apps import UFDLCoreAppConfig
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DockerImageQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of available Docker images.
    """
    pass


class DockerImage(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A Docker image for performing a model-based task.
    """
    # The name of the image
    name = models.CharField(max_length=64)

    # The version of the image
    version = models.CharField(max_length=32)

    # The URL of the image
    url = models.URLField()

    # The URL of the registry in which the image is situated
    registry_url = models.URLField()

    # The username to use to access the registry, or null if none needed
    registry_username = models.CharField(max_length=64, null=True)

    # The password to use to access the registry, or null if none needed
    registry_password = models.CharField(max_length=64, null=True)

    # The CUDA version installed in the image
    cuda_version = models.ForeignKey(f"{UFDLCoreAppConfig.label}.CUDAVersion",
                                     on_delete=models.DO_NOTHING,
                                     related_name="docker_images")

    # The name of the model framework the image is for
    framework = models.CharField(max_length=32)

    # The version of the framework
    framework_version = models.CharField(max_length=16)

    # The domain of the image
    domain = models.CharField(max_length=32)

    # The type of task the image performs
    task = models.CharField(max_length=16)

    # The minimum hardware generation required to run the image
    min_hardware_generation = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Hardware",
                                                on_delete=models.DO_NOTHING,
                                                related_name="+")

    objects = DockerImageQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each image has a unique name/version
            models.UniqueConstraint(name="unique_docker_images",
                                    fields=["name", "version"])
        ]
