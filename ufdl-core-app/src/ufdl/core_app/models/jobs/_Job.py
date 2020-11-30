from typing import Optional, Union, Tuple

from django.db import models
from django.utils.timezone import now

from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig
from ...exceptions import *
from ..files import File
from ..nodes import Node
from .._User import User
from ._JobOutput import JobOutput


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
    template = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.JobTemplate",
        on_delete=models.DO_NOTHING,
        related_name="jobs"
    )

    # The parent job that started this job (if any)
    parent = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Job",
        on_delete=models.DO_NOTHING,
        related_name="children",
        null=True
    )

    # The time the job was started
    start_time = models.DateTimeField(
        null=True,
        default=None,
        editable=False
    )

    # The time the job was finished
    end_time = models.DateTimeField(
        null=True,
        default=None,
        editable=False
    )

    # The body of the error that occurred if the job failed
    error = models.TextField(
        null=True,
        default=None
    )

    # The inputs to the job
    input_values = models.TextField()

    # The arguments to the job template's parameters
    parameter_values = models.TextField(null=True)

    # The worker node executing the job
    node = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Node",
        on_delete=models.DO_NOTHING,
        related_name="jobs",
        null=True,
        default=None
    )

    # A brief description of the job
    description = models.TextField(blank=True)

    objects = JobQuerySet.as_manager()

    # region Lifecycle

    @property
    def is_meta(self) -> bool:
        """
        Whether this job is a meta-job encapsulating other jobs.
        """
        # Local import to avoid circular reference error
        from .meta import MetaTemplate

        return isinstance(self.template.upcast(), MetaTemplate)

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

    @property
    def child_name(self) -> Optional[str]:
        """
        Gets the name of this job in the parent pipeline if it is part
        of one.

        :return:
                    The child name, or None if this job is not a child.
        """
        # If we are not a child, we have no child name
        if self.parent is None:
            return None

        # Get our name from our description
        return self.description[11:].split("'", maxsplit=1)[0]

    def acquire(self, node):
        """
        Allows a node to acquire this job.

        :param node:
                    The node acquiring the job.
        """
        # Can't acquire meta-jobs
        if self.is_meta:
            raise AcquireMetaJobAttempt()

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

        # Mark the parent as started
        if self.parent is not None and not self.parent.is_started:
            self.parent.start(node)

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

        # Mark the job as this node's current job
        if not self.is_meta:
            node.current_job = self
            node.save(update_fields=["current_job"])

    def add_output(
            self,
            name: str,
            type: str,
            data: Union[bytes, File],
            creator: User
    ):
        """
        Adds an output to this job.

        :param name:
                    The name of the output.
        :param type:
                    The type of the output.
        :param data:
                    The data to store in the output file.
        :param creator:
                    The user creating the output.
        :return:
                    The newly-created output.
        """
        # Make sure the job has been started
        if not self.is_started:
            raise JobNotStarted("add_output")

        # Make sure the job isn't already finished
        if self.is_finished:
            raise JobFinished("add_output")

        # Make sure the job doesn't already have an output by this name
        if self.outputs.filter(name=name, type=type).exists():
            raise BadName(name, f"Job already has an output by this name/type ({name}/{type})")

        # Create a file handle to the data if it isn't already one
        if not isinstance(data, File):
            data = File.create(data)

        # Create the output
        output = JobOutput(
            job=self,
            name=name,
            type=type,
            data=data,
            creator=creator
        )
        output.save()

        return output

    def try_create_children(self) -> Tuple[bool, Optional[str]]:
        """
        Attempts to create any sub-jobs of this meta-job if the input is
        available to them.

        :return:
                    Whether all child jobs have finished, and any error
                    that occurred starting children.

        """
        # We don't have children if we're not a meta-job
        if not self.is_meta:
            return True, None

        # Keep track of any errors that occur starting children
        error = None

        # Get our meta-template
        template = self.template.upcast()

        # Get the existing child jobs to this meta-job
        child_jobs = {
            job.child_name: job
            for job in self.children.all()
        }

        # Get the child jobs to this meta-job which have finished
        finished_child_jobs = {
            child_name: job
            for child_name, job in child_jobs.items()
            if job.is_finished
        }

        # Get all expected children of this job
        all_child_relations = {
            child_relation.name: child_relation
            for child_relation in template.child_relations.all()
        }

        # If there aren't any unfinished child-jobs, we're done
        if all(child_name in finished_child_jobs for child_name in all_child_relations.keys()):
            return True, error

        # See if any new child-jobs can be created
        for child_name, child_relation in all_child_relations.items():
            # Skip any jobs that are already created
            if child_name in child_jobs:
                continue

            # Get the names of the dependencies of this template
            dependency_names = {
                dependency.name
                for dependency in template.child_relations.filter(
                    dependencies__dependency=child_relation
                ).all()
            }

            # If all dependencies are finish, create a new sub-job for this child
            if all(dependency_name in finished_child_jobs for dependency_name in dependency_names):
                try:
                    template.create_sub_job(
                        self,
                        child_relation,
                        finished_child_jobs
                    )
                except Exception as e:
                    error = e.args[0]
                    break

        # If we successfully started all the children we could, and there are more to
        # start in future, wait until the next child finishes
        return False, error

    def inherit_child_outputs(self):
        """
        Adds all outputs of child jobs to this job.
        """
        # Get the outputs of all children
        child_outputs = JobOutput.objects.filter(
            job__parent=self
        )

        # Add a copy of each to this meta-job
        for child_output in child_outputs.select_related("job").all():
            JobOutput(
                job=self,
                name=f"{child_output.job.child_name}:{child_output.name}",
                type=child_output.type,
                data=child_output.data,
                creator=child_output.creator
            ).save()

    def finish(self, finisher: Union[Node, 'Job'], error: Optional[str] = None):
        """
        Finishes the job.

        :param finisher:
                    The object finishing the job (either a node or sub-job).
        :param error:
                    Any error that occurred while running the job.
        """
        # Make sure the job has been started
        if not self.is_started:
            raise JobNotStarted("finish")

        # Make sure the job isn't already finished (idempotent for meta-jobs)
        if self.is_finished:
            if self.is_meta:
                return
            else:
                raise JobFinished("finish")

        # If we finished successfully, check if we need to start any more sub-jobs
        if error is None:
            # Try to start any child jobs to this one
            all_children_finished, error = self.try_create_children()

            # This meta-job is not finished if there are remaining children to finish
            if not all_children_finished and error is None:
                return

            # Just before finishing, add all child outputs to this meta-job
            if error is None:
                self.inherit_child_outputs()

        # Mark the job as finished
        self.end_time = now()
        self.error = error
        self.save(update_fields=["end_time", "error"])

        # Clear the current job from this node
        if not self.is_meta:
            finisher.current_job = None
            finisher.save(update_fields=["current_job"])

        # Finish the parent
        if self.parent is not None:
            # If we finished in error, format a related error message for our parent
            parent_error = (
                f"Error in child job '{self.child_name}':\n"
                f"{error}"
                if error is not None else
                None
            )

            self.parent.finish(self, parent_error)

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

        # Reset all errored children
        for child in self.children.filter(error__isnull=False).all():
            child.reset()

    def abort(self):
        """
        Aborts a job.
        """
        # If the job is not acquired, this is a no-op
        if not self.is_acquired:
            return

        # Can't abort a successfully-finished job
        if self.is_finished and self.error is None:
            raise JobFinished("abort")

        # Remove any outputs
        self.outputs.all().delete()

        # Force-remove this job from the acquiring node
        if self.node.current_job == self:
            self.node.current_job = None
            self.node.save(update_fields=['current_job'])

        # Reset the lifecycle to the 'un-acquired' state
        self.start_time = None
        self.end_time = None
        self.error = None
        self.node = None
        self.save(update_fields=['start_time', 'end_time', 'error', 'node'])

    # endregion
