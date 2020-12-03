from typing import Optional, Union, Tuple

from django.db import models
from django.utils.timezone import now

from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ...apps import UFDLCoreAppConfig
from ...exceptions import *
from ..files import File
from ..nodes import Node
from .._User import User
from ._JobOutput import JobOutput, JobOutputQuerySet


class JobQuerySet(SoftDeleteQuerySet):
    """
    A query-set over jobs.
    """
    pass


class Job(SoftDeleteModel):
    """
    A job.

    A job is an instantiation of a job-template with specific settings
    to inform how the work is performed.

    There are 2 types of job, workable jobs (with come from workable templates)
    and meta-jobs (which come from meta-templates). Both types of job have a
    lifecycle with transitions between phases of the lifecycle caused by actions performed by
    clients or worker-nodes executing the job. Workable jobs are designed to be
    performed by external worker nodes, which manage their lifecycle by making
    appropriate calls to the server. Meta-jobs co-ordinate a group of sub-jobs in their
    workflow, and transitions in their lifecycle are triggered by the transitions of
    lifecycle phases in those sub-jobs.

    Workable Job Lifecycle
    ----------------------
    -- Phases --
    Created     := The initial phase of the job's lifecycle.
    Acquired    := The job has been reserved for work by a node.
    Started     := The work of completing a job has been started by the acquiring node.
    Finished    := The job has been successfully completed by the node.
    Errored     := No more work can be done on the job, but it was not completed.

    -- Transitions --
    Created --acquire-> Acquired    := A node reserves the job for work.
    Created --abort-> Created       := A no-op.

    Acquired --release-> Created    := The acquiring node releases the job back to the pool.
    Acquired --abort-> Created      := Equivalent to release.
    Acquired --start-> Started      := The node begins work on the job.

    Started --finish-> Finished     := The node has successfully completed the job.
    Started --error-> Errored       := The node could not complete the job.
    Started --abort-> Created       := The node gives up on the job, or a client steals
                                       the job back from the node.

    Errored --reset-> Acquired      := The node wishes to re-attempt the failed job.
    Errored --abort-> Created       := A client requests that the job be re-attempted.

    Outputs can only be added to jobs in the Started lifecycle-phase, and all outputs
    are removed from a job on any transition except finish.

    Meta-Job Lifecycle
    ------------------
    -- Phases --
    Created     := The initial phase of the job's lifecycle.
    Started     := The work of completing the sub-jobs has begun.
    Finished    := All sub-jobs have successfully completed.
    Errored     := Any sub-job is in the Errored phase.

    -- Transitions --
    Created --start-> Started       := Any sub-job has started.

    Started --start-> Started       := A no-op to make start idempotent.
    Started --finish-> Started      := A no-op if there are unfinished sub-jobs.
    Started --finish-> Finished     := All sub-jobs are in the Finished phase.
    Started --error-> Errored       := Any sub-job is in the Errored phase.

    Errored --start-> Errored       := A no-op to make start idempotent.
    Errored --reset-> Started       := Resets all Errored sub-jobs.
    Errored --finish-> Errored      := A no-op.
    Errored --error-> Errored       := A no-op.

    Finished --finish-> Finished    := A no-op.

    There are no transitions out of the Finished state for either type of job.
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

    @property
    def is_meta(self) -> bool:
        """
        Whether this job is a meta-job encapsulating other jobs.
        """
        # Local import to avoid circular reference error
        from .meta import MetaTemplate

        return isinstance(self.template.upcast(), MetaTemplate)

    @property
    def child_name(self) -> str:
        """
        Gets the name of this job in the parent workflow.

        :return:
                    The child name.
        """
        assert self.parent is not None, "Job is not a child"

        # Get our name from our description
        return self.description[11:].split("'", maxsplit=1)[0]

    # region Lifecycle Phases

    @property
    def is_created(self) -> bool:
        """
        Whether this job is in the Created phase.
        """
        return self.start_time is None and self.node is None

    @property
    def is_acquired(self) -> bool:
        """
        Whether this job is in the Acquired phase.
        """
        # Meta-jobs have no Acquired phase
        if self.is_meta:
            raise Exception("Meta-jobs have no Acquired phase")
        return self.start_time is None and self.node is not None

    @property
    def is_started(self) -> bool:
        """
        Whether this job is in the Started phase.
        """
        return self.start_time is not None and self.end_time is None

    @property
    def is_finished(self) -> bool:
        """
        Whether this job is in the Finished phase.
        """
        return self.end_time is not None and self.error is None

    @property
    def is_errored(self):
        """
        Whether the job is in the Errored phase
        """
        return self.error is not None

    @property
    def lifecycle_phase(self) -> str:
        """
        Gets the name of the job's current lifecycle phase.
        """
        if self.is_created:
            return "Created"
        elif self.is_started:
            return "Started"
        elif self.is_finished:
            return "Finished"
        elif self.is_errored:
            return "Errored"
        elif self.is_meta and self.is_acquired:
            return "Acquired"
        else:
            raise Exception(
                f"Failed to determine lifecycle phase of job\n"
                f"{self}"
            )

    # endregion

    # region Lifecycle Transitions

    def acquire(self, node: Node):
        """
        Allows a node to acquire this job.

        :param node:
                    The node acquiring the job.
        """
        assert not self.is_meta, "Can't acquire meta-job"

        self._acquire_workable(node)

    def _acquire_workable(self, node):
        assert not self.is_meta, "_acquire_workable called on meta-job"

        # Only valid from the Created phase
        if not self.is_created:
            raise IllegalPhaseTransition(self, "acquire", "Job has already been acquired")

        self.node = node
        self.save(update_fields=['node'])

    def release(self):
        """
        Releases an acquired job.
        """
        assert not self.is_meta, "Can't release meta-job"

        self._release_workable()

    def _release_workable(self):
        assert not self.is_meta, "_release_workable called on meta-job"

        # Can only release from the Acquired phase
        if not self.is_acquired:
            raise IllegalPhaseTransition(self, "release", "Can only release from the Acquired phase")

        # Mark the job as un-acquired
        self.node = None
        self.save(update_fields=['node'])

    def start(self, node):
        """
        Starts the job.
        """
        assert not self.is_meta, "Can't manually start meta-job"

        self._start_workable(node)

    def _start_meta(self):
        assert self.is_meta, "_start_meta called on workable job"
        assert not self.is_finished, "_start_meta called on finished meta-job"

        # Idempotent
        if not self.is_created:
            return

        # Start the parent meta-job, if any
        if self.parent is not None:
            self.parent._start_meta()

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

    def _start_workable(self, node: Node):
        assert not self.is_meta, "_start_workable called on meta-job"

        # Can only start from the Acquired phase
        if not self.is_acquired:
            raise IllegalPhaseTransition(self, "start", "Can only start from the Acquired phase")

        # Make sure the node isn't already working a job
        if node.is_working_job:
            raise NodeAlreadyWorking()

        assert self.node == node, "_start_workable called by another node"

        # Start the parent meta-job, if any
        if self.parent is not None:
            self.parent._start_meta()

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

        # Mark the job as this node's current job
        node.current_job = self
        node.save(update_fields=["current_job"])

    def finish(self, node: Node):
        """
        Finishes a job.

        :param node:
                    The node finishing the job.
        """
        assert not self.is_meta, "finish called on meta-job"

        self._finish_workable(node)

    def _finish_meta(self, outputs: JobOutputQuerySet):
        assert self.is_meta, "_finish_meta called on workable job"
        assert not self.is_created, "_finish_meta called in the Created phase"
        assert not self.is_finished, "_finish_meta called in the Finished phase"

        # Attach the given outputs
        for output in outputs.select_related("job").all():
            JobOutput(
                job=self,
                name=f"{output.job.child_name}:{output.name}",
                type=output.type,
                data=output.data,
                creator=output.creator
            ).save()

        # Try to start any child jobs to this one
        all_children_finished, error = self._try_create_children()

        # If an error occurred creating children, fail this meta-job
        if error is not None:
            self._finish_with_error_meta(f"Error creating child-jobs: {error}")

        # If the meta-job is in the Errored phase, nothing more required
        if self.is_errored:
            return

        # This meta-job is not finished if there are remaining children to finish
        if not all_children_finished:
            return

        # Mark the job as finished
        self.end_time = now()
        self.save(update_fields=["end_time"])

        # Let our parent know we've finished
        if self.parent is not None:
            self.parent._finish_meta(self.outputs)

    def _finish_workable(self, node: Node):
        assert node.current_job == self, "_finish_workable called with incorrect node"

        # Clear the current job from this node
        node.current_job = None
        node.save(update_fields=["current_job"])

        # If this job has been removed from the node, stop here
        if self.node != node:
            return

        # Make sure the job has been started
        if not self.is_started:
            raise IllegalPhaseTransition(self, "finish", "Job not in the Started phase")

        # Mark the job as finished
        self.end_time = now()
        self.save(update_fields=["end_time"])

        # Finish the parent if we have one
        if self.parent is not None:
            self.parent._finish_meta(self.outputs)

    def finish_with_error(self, node: Node, error: str):
        """
        Finishes the job with an error.

        :param node:
                    Then node finishing the job.
        :param error:
                    The error that occurred.
        """
        assert not self.is_meta, "finish_with_error called on meta-job"

        self._finish_with_error_workable(node, error)

    def _finish_with_error_meta(self, error: str):
        assert self.is_meta, "_finish_meta called on workable job"
        assert not self.is_created, "_finish_meta called in the Created phase"
        assert not self.is_finished, "_finish_meta called in the Finished phase"

        # If the meta-job is in the Errored phase, nothing more required
        if self.is_errored:
            return

        # Mark the job as finished
        self.end_time = now()
        self.error = error
        self.save(update_fields=["end_time", "error"])

        # Let our parent know we've finished
        if self.parent is not None:
            self.parent._finish_with_error_meta(self._format_error_for_parent(error))

    def _finish_with_error_workable(self, node: Node, error: str):
        assert node.current_job == self, "_finish_with_error_workable called with incorrect node"

        # Clear the current job from this node
        node.current_job = None
        node.save(update_fields=["current_job"])

        # If this job has been removed from the node, stop here
        if self.node != node:
            return

        # Make sure the job has been started
        if not self.is_started:
            raise IllegalPhaseTransition(self, "finish", "Job not in the Started phase")

        # Mark the job as errored
        self.end_time = now()
        self.error = error
        self.save(update_fields=["end_time", "error"])

        # Error the parent if we have one
        if self.parent is not None:
            self.parent._finish_with_error_meta(self._format_error_for_parent(error))

    def reset(self, attempt_reset_parent: bool = True):
        """
        Resets a job.
        """
        if self.is_meta:
            return self._reset_meta(attempt_reset_parent)
        else:
            return self._reset_workable(attempt_reset_parent)

    def _reset_meta(self, attempt_reset_parent: bool = True):
        assert self.is_meta, "_reset_meta called on workable job"

        # Make sure the job is in the Errored phase
        if not self.is_errored:
            raise IllegalPhaseTransition(self, "reset", "Job is not in the Errored phase")

        # Reset all errored children
        for child in self.children.filter(error__isnull=False).all():
            child.reset(False)

        # Reset the lifecycle to the Started phase
        self.end_time = None
        self.error = None
        self.save(update_fields=['end_time', 'error'])

        if attempt_reset_parent:
            self._attempt_reset_parent()

    def _reset_workable(self, attempt_reset_parent: bool = True):
        assert not self.is_meta, "_reset_workable called on meta-job"

        # Make sure the job is in the Errored phase
        if not self.is_errored:
            raise IllegalPhaseTransition(self, "reset", "Job is not in the Errored phase")

        # Remove any outputs
        self.outputs.all().delete()

        # Reset the lifecycle to the Acquired phase
        self.start_time = None
        self.end_time = None
        self.error = None
        self.save(update_fields=['start_time', 'end_time', 'error'])

        if attempt_reset_parent:
            self._attempt_reset_parent()

    def abort(self):
        """
        Aborts a job.
        """
        assert not self.is_meta, "abort called on meta-job"

        return self._abort_workable()

    def _abort_workable(self):
        assert not self.is_meta, "_abort_workable called on meta-job"

        # If the job is in the Created phase, this is a no-op
        if self.is_created:
            return

        # If the job is in the Acquired phase, this is a release
        if self.is_acquired:
            self._release_workable()
            return

        # If the job is in the Errored phase, this is a reset and release
        if self.is_errored:
            self._reset_workable()
            self._release_workable()
            return

        # Can't abort a successfully-finished job
        if self.is_finished:
            raise IllegalPhaseTransition(self, "abort", "Can't abort a successfully-completed job")

        assert self.is_started, "_abort_workable not in Started phase"

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

    def _try_create_children(self) -> Tuple[bool, Optional[str]]:
        """
        Attempts to create any sub-jobs of this meta-job if the input is
        available to them.

        :return:
                    Whether all child jobs have finished, and any error
                    that occurred starting children.
        """
        # Keep track of any errors that occur starting children
        error = None

        # We don't have children if we're not a meta-job
        if not self.is_meta:
            return True, error

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

            # If all dependencies are finished, create a new sub-job for this child
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

    def _format_error_for_parent(self, error: str) -> str:
        """
        Formats the given error message for the parent job.

        :param error:
                    The error message to format.
        :return:
                    The message formatted for the parent.
        """
        return (
            f"Error in child job '{self.child_name}':\n"
            f"{error}"
        )

    def _attempt_reset_parent(self):
        """
        Attempts to reset the parent job.
        """
        parent = self.parent
        if parent is not None:
            if not parent.children.filter(error__isnull=False).exists():
                parent.end_time = None
                parent.error = None
                parent.save(update_fields=['start_time', 'end_time', 'error'])
