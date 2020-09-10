from django.db import models
from simple_django_teams.mixins import SoftDeleteModel

from ...apps import UFDLCoreAppConfig
from ..mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class DockerImageToJobTypeQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    Additional functionality for working with query-sets of Docker-image tasks.
    """
    pass


class DockerImageToJobType(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Model relating docker-images to the tasks they perform.
    """
    # The Docker image
    docker_image = models.ForeignKey(f"{UFDLCoreAppConfig.label}.DockerImage",
                                     on_delete=models.DO_NOTHING,
                                     related_name="+")

    # The reference to the file's data
    job_type = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobType",
                                 on_delete=models.DO_NOTHING,
                                 related_name="+")

    objects = DockerImageToJobTypeQuerySet.as_manager()
