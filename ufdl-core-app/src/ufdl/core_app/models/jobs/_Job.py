from typing import Optional

from django.db import models
from django.utils.timezone import now

from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig
from ...exceptions import *


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
        Allows a node to acquire this job.

        :param node:    The node acquiring the job.
        """
        # Make sure the job isn't already acquired
        if self.is_acquired:
            raise JobAcquired()

        self.node = node
        self.save(update_fields=['node'])

    def release(self):
        """
        Releases a job.
        """
        # Make sure that we have acquired the job
        if self.node is None:
            raise JobNotAcquired()

        # Make sure the job hasn't already been started
        if self.is_started:
            raise JobStarted("release")

        # Mark the job as un-acquired
        self.node = None
        self.save(update_fields=['node'])

    def start(self, node):
        """
        Starts the job.
        """
        # Make sure the job hasn't already been started
        if self.is_started:
            raise JobStarted("start")

        # Make sure the node isn't already working a job
        if node.is_working_job:
            raise NodeAlreadyWorking()

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

        # Mark the job as this node's current job
        node.current_job = self
        node.save(update_fields=["current_job"])

    def finish(self, node, error: Optional[str] = None):
        """
        Finishes the job.

        :param node:    The node running the job.
        :param error:   Any error that occurred while running the job.
        """
        # Make sure the job has been started
        if not self.is_started:
            raise JobNotStarted("finish")

        # Make sure the job isn't already finished
        if self.is_finished:
            raise JobFinished("finish")

        # Mark the job as finished
        self.end_time = now()
        self.error = error
        self.save(update_fields=["end_time", "error"])

        # Clear the current job from this node
        node.current_job = None
        node.save(update_fields=["current_job"])

    def reset(self):
        """
        Resets a job.
        """
        # Make sure the job is finished
        if not self.is_finished:
            raise JobNotFinished("reset")

        # If the job completed without error, it cannot be reset
        if self.error is not None:
            raise JobFinished("reset")

        # Remove any outputs
        self.outputs.all().delete()

        # Reset the lifecycle to the 'acquired' state
        self.start_time = None
        self.end_time = None
        self.error = None
        self.save(update_fields=['start_time', 'end_time', 'error'])

    def abort(self):
        """
        Aborts a job.
        """
        # If the job is not acquired, this is a no-op
        if not self.is_acquired:
            return

        # Remove any outputs
        self.outputs.all().delete()

        # Force-remove this job from the acquiring node
        self.node.current_job = None
        self.node.save(update_fields=['current_job'])

        # Reset the lifecycle to the 'un-acquired' state
        self.start_time = None
        self.end_time = None
        self.error = None
        self.node = None
        self.save(update_fields=['start_time', 'end_time', 'error', 'node'])
