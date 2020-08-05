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
    url = models.CharField(max_length=200)

    # The URL of the registry in which the image is situated
    registry_url = models.CharField(max_length=200)

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
                                                related_name="+",
                                                null=True)

    # Whether the Docker image can run on a CPU-only machine (no GPU)
    cpu = models.BooleanField(default=False)

    @property
    def name_and_version(self) -> str:
        return f"{self.name} v{self.version}"

    objects = DockerImageQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each image has a unique name/version
            models.UniqueConstraint(name="unique_docker_images",
                                    fields=["name", "version"])
        ]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Check that the 'min_hardware_generation' is only null if 'cpu' is true
        if self.min_hardware_generation is None and not self.cpu:
            raise Exception(f"min_hardware_generation can't be null is cpu is false (for '{self.name}')")

        super().save(force_insert, force_update, using, update_fields)
