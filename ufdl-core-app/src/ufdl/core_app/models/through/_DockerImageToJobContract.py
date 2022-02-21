from django.db import models

from ...apps import UFDLCoreAppConfig
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DockerImageToJobContractQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    Additional functionality for working with query-sets of Docker-image tasks.
    """
    pass


class DockerImageToJobContract(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Model relating docker-images to the tasks they perform.
    """
    # The Docker image
    docker_image = models.ForeignKey(f"{UFDLCoreAppConfig.label}.DockerImage",
                                     on_delete=models.DO_NOTHING,
                                     related_name="+")

    # The contract that the image can fulfil
    job_contract = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobContract",
                                     on_delete=models.DO_NOTHING,
                                     related_name="+")

    objects = DockerImageToJobContractQuerySet.as_manager()
