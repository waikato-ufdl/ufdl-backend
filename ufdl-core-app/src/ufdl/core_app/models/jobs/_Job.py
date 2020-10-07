from typing import Optional

from django.db import models
from django.utils.timezone import now

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

    # A brief description of the job
    description = models.TextField(blank=True)

    objects = JobQuerySet.as_manager()

    @property
    def is_acquired(self) -> bool:
        """
        Whether this job has already been acquired by a node.
        """
        return self.node is not None

    @property
    def is_started(self) -> bool:
        """
        Whether the job has been started.
        """
        return self.start_time is not None

    @property
    def is_finished(self) -> bool:
        """
        Whether the job is already finished.
        """
        return self.end_time is not None

    def acquire(self, node):
        """
        Acquires the job.

        :param node:    The node acquiring the job.
        """
        self.node = node
        self.save(update_fields=['node'])

    def start(self):
        """
        Starts the job.
        """
        self.start_time = now()
        self.save(update_fields=["start_time"])

    def finish(self, error: Optional[str] = None):
        """
        Finishes the job.

        :param error:   Any error that occurred while running the job.
        """
        self.end_time = now()
        self.error = error
        self.save(update_fields=["end_time", "error"])

    def reset(self):
        """
        Resets the job.
        """
        # Remove any outputs
        self.outputs.all().delete()

        # Reset the lifecycle state
        self.node = None
        self.start_time = None
        self.end_time = None
        self.error = None
        self.save(update_fields=['node', 'start_time', 'end_time', 'error'])
