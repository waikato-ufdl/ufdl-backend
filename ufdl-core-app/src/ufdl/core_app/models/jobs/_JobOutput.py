from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig


class JobOutputQuerySet(SoftDeleteQuerySet):
    """
    A query-set over job outputs.
    """
    pass


class JobOutput(SoftDeleteModel):
    """
    An output from a job.
    """
    # The job which created this output
    job = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Job",
                            on_delete=models.DO_NOTHING,
                            related_name="outputs")

    # The name of the output
    name = models.CharField(max_length=200)

    # The type of output
    type = models.CharField(max_length=64)

    # The output data
    data = models.ForeignKey(f"{UFDLCoreAppConfig.label}.FileReference",
                             on_delete=models.DO_NOTHING,
                             related_name="+")

    objects = JobOutputQuerySet.as_manager()
