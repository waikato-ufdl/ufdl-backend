from django.db import models
from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig


class JobQuerySet(SoftDeleteQuerySet):
    """
    A query-set over jobs.
    """
    pass


class Job(SoftDeleteModel):
    """
    A job.
    """
    # The template on which the job is based
    template = models.ForeignKey(f"{UFDLCoreAppConfig.label}.JobTemplate",
                                 on_delete=models.DO_NOTHING,
                                 related_name="jobs")

    # The Docker image to execute the job
    docker_image = models.ForeignKey(f"{UFDLCoreAppConfig.label}.DockerImage",
                                     on_delete=models.DO_NOTHING,
                                     related_name="jobs")

    # The time the job was started
    start_time = models.DateTimeField(null=True,
                                      default=None,
                                      editable=False)

    # The time the job was finished
    end_time = models.DateTimeField(null=True,
                                    default=None,
                                    editable=False)

    # The body of the error that occurred if the job failed
    error = models.TextField(null=True, default=None)

    # The inputs to the job
    input_values = models.TextField()

    # The arguments to the job template's parameters
    parameter_values = models.TextField(blank=True)

    # The worker node executing the job
    node = models.ForeignKey(f"{UFDLCoreAppConfig.label}.Node",
                             on_delete=models.DO_NOTHING,
                             related_name="jobs",
                             null=True,
                             default=None)

    objects = JobQuerySet.as_manager()
