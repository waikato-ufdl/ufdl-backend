from enum import Enum
from typing import Optional, Union, Tuple, Dict

from django.db import models
from django.utils.timezone import now

from simple_django_teams.mixins import SoftDeleteModel, SoftDeleteQuerySet

from ufdl.json.core.jobs.notification import (
    NotificationActions,
    NotificationOverride as JSONNotificationOverride
)

from wai.json.raw import RawJSONElement, RawJSONObject

from ...apps import UFDLCoreAppConfig
from ...exceptions import *
from ...settings import core_settings
from ..files import File
from ..nodes import Node
from .._User import User
from .notifications import *
from ._JobOutput import JobOutput, JobOutputQuerySet


class LifecyclePhase(Enum):
    """
    The phases of a job's lifecycle.
    """
    CREATED = 0
    STARTED = 1
    FINISHED = 2
    ERRORED = 3
    CANCELLED = 4


class JobQuerySet(SoftDeleteQuerySet):
    """
    A query-set over jobs.
    """
    pass


class Job(SoftDeleteModel):
    """
    A job is an instantiation of a job-template with specific settings
    to inform how the work is performed.

    There are 2 types of job, workable jobs (which come from workable templates)
    and meta-jobs (which come from meta-templates). Both types of job have a
    lifecycle with transitions between phases of the lifecycle caused by actions performed by
    clients or worker-nodes executing the job. Workable jobs are designed to be
    performed by external worker nodes, which manage their lifecycle by making
    appropriate calls to the server (a node must first 'acquire' the job before it can
    make these calls). Meta-jobs co-ordinate a group of sub-jobs in their
    workflow, and transitions in their lifecycle are triggered by the transitions of
    lifecycle phases in those sub-jobs.

    Job Lifecycle
    ----------------------
    -- Phases --
    CREATED     := The initial phase of the job's lifecycle.
    STARTED     := The work of completing a job has been started.
    FINISHED    := The job has been successfully completed.
    ERRORED     := No more work can be done on the job, but it was not completed.
    CANCELLED   := The job was cancelled by the client.

    -- Transitions --
    Start       :=  Work on completing the job has begun.
                    Meta: Triggered by any child job starting.
                    Phases: CREATED --> STARTED
    Progress    :=  Some progress has been made on a job.
                    Meta: Triggered by progress on any child job.
                    Phases: STARTED --> STARTED
    Finish      :=  The job has been successfully completed.
                    Meta: Triggered when the last child job has successfully completed.
                    Phases: STARTED --> FINISHED
                            CANCELLED --> CANCELLED (a no-op)
    Error       :=  The job cannot proceed due to some problem.
                    Meta: Triggered by an error transition in any child job.
                    Phases: STARTED --> ERRORED
                            CANCELLED --> CANCELLED (a no-op)
    Reset       :=  The error preventing progress has been potentially cleared.
                    Meta: Triggered by resetting a child job, only proceeds if there are no
                          errored sibling jobs.
                    Phases: ERRORED --> STARTED
    Abort       :=  Returns the job to its initial state. Used to reset jobs that have been
                    locked by nodes that have gone offline.
                    Meta: Meta-jobs cannot be aborted.
                    Phases: CREATED --> CREATED
                            STARTED, ERRORED --> STARTED
    Cancel      :=  The job is no longer needed.
                    Meta: If the job is part of a heirarchy, only the top-level meta-job can
                          be cancelled, and it automatically cancels all child jobs.
                    Phases: CREATED, STARTED, ERRORED --> CANCELLED
                            FINISHED --> FINISHED (no-op)
                            CANCELLED --> CANCELLED (no-op)

    Outputs can only be added to jobs in the Started lifecycle-phase, and all outputs
    are removed from a job when it is reset/aborted.
    """
    # region Static Fields

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

    # A brief description of the job
    description = models.TextField(blank=True)

    # The inputs to the job
    input_values = models.TextField()

    # The arguments to the job template's parameters
    parameter_values = models.TextField(null=True)

    # endregion

    # region Lifecycle Fields

    # The worker node that has acquired the job
    node = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Node",
        on_delete=models.DO_NOTHING,
        related_name="jobs",
        null=True,
        default=None
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
    error_reason = models.TextField(
        null=True,
        default=None
    )

    # The last progress made on the job
    progress_amount = models.FloatField(default=0.0)

    # endregion

    objects = JobQuerySet.as_manager()

    # region Static Properties

    @property
    def is_meta(self) -> bool:
        """
        Whether this job is a meta-job encapsulating other jobs.
        """
        # Local import to avoid circular reference error
        from .meta import MetaTemplate

        return isinstance(self.template.upcast(), MetaTemplate)

    @property
    def has_parent(self) -> bool:
        """
        Whether this job has a parent job.
        """
        return self.parent is not None

    @property
    def child_name(self) -> str:
        """
        Gets the name of this job in the parent workflow.

        :return:
                    The child name.
        """
        assert self.has_parent, "Job is not a child"

        # Get our name from our description
        return self.description[11:].split("'", maxsplit=1)[0]

    @property
    def full_child_name(self) -> str:
        """
        Gets the fully-qualified child name of this job in
        the outermost parent job.

        :return:
                    The fully-qualified child name.
        """
        assert self.has_parent, "Job is not a child"

        return ":".join(map(lambda job: job.child_name, self.parent_hierarchy[1:]))

    @property
    def parent_hierarchy(self) -> Tuple['Job', ...]:
        """
        Gets the hierarchy of jobs that this job is part of,
        from outermost parent to this job (inclusive).
        """
        return (
            (*self.parent.parent_hierarchy, self)
            if self.has_parent else
            (self,)
        )

    @property
    def top_level_parent(self) -> 'Job':
        """
        Gets the top-level parent job in the job hierarchy that this
        job participates in.
        """
        return self.parent_hierarchy[0]

    @property
    def websocket_group_name(self) -> str:
        """
        The name of the group that this job should broadcast transitions to.
        """
        return f"Job-{self.pk}"

    # endregion

    @property
    def is_acquired(self) -> bool:
        """
        Whether this job has been acquired.
        """
        # Meta-jobs have no Acquired phase
        assert not self.is_meta, "Meta-jobs cannot be acquired"

        return self.node is not None

    # region Lifecycle Phases

    @property
    def lifecycle_phase(self) -> LifecyclePhase:
        """
        Gets the name of the job's current lifecycle phase.
        """
        if self.start_time is None:
            return LifecyclePhase.CREATED
        elif self.end_time is None:
            if self.error_reason is None:
                return LifecyclePhase.STARTED
            else:
                return LifecyclePhase.CANCELLED
        else:
            if self.error_reason is None:
                return LifecyclePhase.FINISHED
            else:
                return LifecyclePhase.ERRORED

    @property
    def is_created(self) -> bool:
        """
        Whether this job is in the CREATED phase.
        """
        return self.lifecycle_phase is LifecyclePhase.CREATED

    @property
    def is_started(self) -> bool:
        """
        Whether this job is in the STARTED phase.
        """
        return self.lifecycle_phase is LifecyclePhase.STARTED

    @property
    def is_finished(self) -> bool:
        """
        Whether this job is in the FINISHED phase.
        """
        return self.lifecycle_phase is LifecyclePhase.FINISHED

    @property
    def is_errored(self):
        """
        Whether the job is in the ERRORED phase.
        """
        return self.lifecycle_phase is LifecyclePhase.ERRORED

    @property
    def is_cancelled(self):
        """
        Whether the job is in the CANCELLED phase.
        """
        return self.lifecycle_phase is LifecyclePhase.CANCELLED

    @property
    def has_been_started(self):
        """
        Whether this job has been started (not necessarily still
        in the STARTED phase).
        """
        return self.start_time is not None

    @property
    def has_been_finalised(self) -> bool:
        """
        Whether this job is in a finalised state (FINISHED/CANCELLED).
        """
        return self.lifecycle_phase in {LifecyclePhase.FINISHED, LifecyclePhase.CANCELLED}

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

    def _acquire_workable(self, node: Node):
        assert not self.is_meta, "_acquire_workable called on meta-job"

        # Cannot acquire an acquired job, unless it's acquired by the calling
        # node, in which case it's a no-op
        acquiring_node = self.node
        if acquiring_node == node:
            return
        elif acquiring_node is not None:
            raise JobAcquired(self)

        # Cannot acquire a finalised job
        if self.has_been_finalised:
            raise IllegalPhaseTransition(self, "acquire", "Job has already been finalised")

        self.node = node
        self.save(update_fields=['node'])

        self._perform_notifications(Transition.ACQUIRE)

    def release(self, node: Node):
        """
        Releases an acquired job.
        """
        assert not self.is_meta, "Can't release meta-job"

        self._release_workable(node)

    def _release_workable(self, node: Node):
        assert not self.is_meta, "_release_workable called on meta-job"
        assert node.current_job != self, "_release_workable called on job in progress"

        # Releasing a job that is not acquired by the calling node is a no-op
        if self.node != node:
            return

        if self.lifecycle_phase not in [LifecyclePhase.CREATED, LifecyclePhase.ERRORED]:
            raise IllegalPhaseTransition(self, "release", "Can't release a started or finalised job")

        # Mark the job as un-acquired
        self.node = None
        self.save(update_fields=['node'])

        self._perform_notifications(Transition.RELEASE)

    def start(self, node: Node):
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
        if self.has_parent:
            self.parent._start_meta()

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

        self._perform_notifications(Transition.START)

    def _start_workable(self, node: Node):
        assert not self.is_meta, "_start_workable called on meta-job"
        assert self.node == node, "_start_workable called from non-acquiring node"

        # Make sure the node isn't already working a job
        if node.is_working_job:
            raise NodeAlreadyWorking()

        # Can only start from the CREATED phase
        if not self.is_created:
            raise IllegalPhaseTransition(self, "start", "Job already started")

        assert self.node == node, "_start_workable called by another node"

        # Start the parent meta-job, if any
        if self.has_parent:
            self.parent._start_meta()

        # Mark the job as started
        self.start_time = now()
        self.save(update_fields=["start_time"])

        # Mark the job as this node's current job
        node.current_job = self
        node.save(update_fields=["current_job"])

        self._perform_notifications(Transition.START)

    def progress(self, node: Node, progress: float, **other: RawJSONElement):
        """
        Updates any followers of the job on progress toward completion.

        :param progress:
                    The percentage of completion, from 0.0 -> 1.0.
        :param other:
                    Any other progress meta-data.
        """
        assert not self.is_meta, "Can't manually progress meta-job"

        self._progress_workable(node, progress, **other)

    def _progress_meta(self, **other: RawJSONElement):
        assert self.is_meta, "_progress_meta called on workable job"
        assert self.is_started, "_progress_meta called on job not in started phase"

        # Progress is the average child progress (including as-yet-uncreated children)
        progress = self.children.aggregate(
            total=models.Sum("progress_amount")
        )['total'] / self.template.num_children

        # Update our progress amount
        self.progress_amount = progress
        self.save(update_fields=['progress_amount'])

        self._perform_notifications(Transition.PROGRESS, **other)

        if self.has_parent:
            self.parent._progress_meta(
                triggered_by=self.pk,
                progress=progress,
                in_turn=other
            )

    def _progress_workable(self, node: Node, progress: float, **other: RawJSONElement):
        assert not self.is_meta, "_progress_workable called on meta-job"
        assert node.current_job == self, "_progress_workable called by incorrect node"
        assert self.node == node, "_progress_workable called by another node"

        # Can only progress from the Started phase
        if not self.is_started:
            raise IllegalPhaseTransition(self, "progress", "Can only progress from the STARTED phase")

        # Progress value must be in [0.0, 1.0]
        if not (0.0 <= progress <= 1.0):
            raise BadArgumentValue(
                "progress",
                "progress",
                str(progress),
                reason="progress must be in [0.0, 1.0]"
            )

        # Update our progress amount
        self.progress_amount = progress
        self.save(update_fields=['progress_amount'])

        self._perform_notifications(Transition.PROGRESS, **other)

        if self.has_parent:
            self.parent._progress_meta(
                triggered_by=self.pk,
                progress=progress
            )

    def finish(self, node: Node):
        """
        Finishes a job.

        :param node:
                    The node finishing the job.
        """
        assert not self.is_meta, "Cannot manually finish a meta-job"

        self._finish_workable(node)

    def _finish_meta(self, outputs: JobOutputQuerySet):
        assert self.is_meta, "_finish_meta called on workable job"
        assert not self.is_created, "_finish_meta called in the CREATED phase"
        assert not self.is_finished, "_finish_meta called in the FINISHED phase"

        # Attach the given outputs
        for output in outputs.select_related("job").all():
            JobOutput(
                job=self,
                name=f"{output.job.child_name}:{output.name}",
                type=output.type,
                data=output.data,
                creator=output.creator
            ).save()

        # If this job has been cancelled, nothing more is required
        if self.is_cancelled:
            return

        # Try to start any child jobs to this one
        all_children_finished, error = self._try_create_children()

        # If an error occurred creating children, fail this meta-job
        if error is not None:
            self._error_meta(f"Error creating child-jobs: {error}")

        # If the meta-job is in the Errored phase, nothing more required
        if self.is_errored:
            return

        # This meta-job is not finished if there are remaining children to finish
        if not all_children_finished:
            return

        # Mark the job as finished
        self.end_time = now()
        self.save(update_fields=["end_time"])

        self._perform_notifications(Transition.FINISH)

        # Let our parent know we've finished
        if self.has_parent:
            self.parent._finish_meta(self.outputs)

    def _finish_workable(self, node: Node):
        assert node.current_job == self, "_finish_workable called with incorrect node"

        # Clear the current job from this node
        node.current_job = None
        node.save(update_fields=["current_job"])

        # If this job has been removed from the node, or the
        # job has been cancelled, stop here
        if self.node != node or self.is_cancelled:
            return

        # Make sure the job has been started
        if not self.is_started:
            raise IllegalPhaseTransition(self, "finish", "Job not in the Started phase")

        # Mark the job as finished
        self.end_time = now()
        self.save(update_fields=["end_time"])

        # Fire notifications
        self._perform_notifications(Transition.FINISH)

        # Finish the parent if we have one
        if self.has_parent:
            self.parent._finish_meta(self.outputs)

    def error(self, node: Node, error: str):
        """
        Finishes the job with an error.

        :param node:
                    Then node finishing the job.
        :param error:
                    The error that occurred.
        """
        assert not self.is_meta, "error called on meta-job"

        self._error_workable(node, error)

    def _error_meta(self, error: str):
        assert self.is_meta, "_error_meta called on workable job"
        assert not self.is_created, "_error_meta called in the Created phase"
        assert not self.is_finished, "_error_meta called in the Finished phase"
        assert not self.is_cancelled, "_error_meta called in the Cancelled phase"

        # If the meta-job is in the Errored phase, nothing more required
        if self.is_errored:
            return

        # Mark the job as finished
        self.end_time = now()
        self.error_reason = error
        self.save(update_fields=["end_time", "error_reason"])

        self._perform_notifications(Transition.ERROR)

        # Let our parent know we've finished
        if self.has_parent:
            self.parent._error_meta(self._format_error_for_parent(error))

    def _error_workable(self, node: Node, error: str):
        assert node.current_job == self, "_error_workable called with incorrect node"

        # Clear the current job from this node
        node.current_job = None
        node.save(update_fields=["current_job"])

        # If this job has been removed from the node, or the
        # job has been cancelled, stop here
        if self.node != node or self.is_cancelled:
            return

        # Make sure the job has been started
        if not self.is_started:
            raise IllegalPhaseTransition(self, "error", "Job not in the Started phase")

        # Mark the job as errored
        self.end_time = now()
        self.error_reason = error
        self.save(update_fields=["end_time", "error_reason"])

        self._perform_notifications(Transition.ERROR)

        # Error the parent if we have one
        if self.has_parent:
            self.parent._error_meta(self._format_error_for_parent(error))

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
            raise IllegalPhaseTransition(self, "reset", "Job is not in the ERRORED phase")

        # Reset all errored children
        for child in self.children.filter(error__isnull=False).all():
            child.reset(False)

        # Reset the lifecycle to the Started phase
        self.end_time = None
        self.error_reason = None
        self.save(update_fields=['end_time', 'error_reason'])

        self._perform_notifications(Transition.RESET)

        if attempt_reset_parent:
            self._attempt_reset_parent()

    def _reset_workable(self, attempt_reset_parent: bool = True):
        assert not self.is_meta, "_reset_workable called on meta-job"

        # Make sure the job is in the ERRORED phase
        if not self.is_errored:
            raise IllegalPhaseTransition(self, "reset", "Job is not in the ERRORED phase")

        # Remove any outputs
        self.outputs.all().delete()

        # Reset the lifecycle to the Acquired phase
        self.end_time = None
        self.error_reason = None
        self.save(update_fields=['end_time', 'error_reason'])

        self._perform_notifications(Transition.RESET)

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

        # Can't abort a finalised job
        if self.has_been_finalised:
            raise IllegalPhaseTransition(self, "abort", "Can't abort a finalised job")

        # Remove any outputs
        self.outputs.all().delete()

        # Reset the lifecycle to the 'un-acquired' state
        self.end_time = None
        self.error_reason = None
        self.node = None
        self.save(update_fields=['end_time', 'error_reason', 'node'])

        self._perform_notifications(Transition.ABORT)

    def cancel(self, called_from_parent: bool = False):
        """
        Cancels a job.

        :param called_from_parent
                    Whether the parent is cancelling its children.
        """
        if self.is_meta:
            self._cancel_meta(called_from_parent)
        else:
            self._cancel_workable(called_from_parent)

    def _cancel_meta(self, called_from_parent: bool):
        # No-op if already finalised
        if self.has_been_finalised:
            return

        # Must be the top-level parent
        if not called_from_parent and self.has_parent:
            raise IllegalPhaseTransition(self, "cancel", "Job is a child job")

        # Perform the transition
        self.end_time = None
        self.error_reason = "Cancelled"
        self.save(update_fields=['end_time', 'error_reason'])

        # Cancel all child jobs
        for child in self.children.all():
            child.cancel(True)

        # Fire notifications
        self._perform_notifications(Transition.CANCEL)

    def _cancel_workable(self, called_from_parent: bool):
        # No-op if already finalised
        if self.has_been_finalised:
            return

        # Must be the top-level parent
        if not called_from_parent and self.has_parent:
            raise IllegalPhaseTransition(self, "cancel", "Job is a child job")

        # Perform the transition
        self.end_time = None
        self.error_reason = "Cancelled"
        self.save(update_fields=['end_time', 'error_reason'])

        # Fire notifications
        self._perform_notifications(Transition.CANCEL)

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
        if not self.has_been_started:
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
                parent.save(update_fields=['end_time', 'error'])

    # region Notifications

    def attach_notification_overrides(self, overrides: Dict[str, JSONNotificationOverride]):
        """
        Attaches notification overrides for child jobs to this job. Only valid
        for meta-jobs that are top-level in their job-hierarchy.

        :param overrides:
                    The dictionary from children names to overrides.
        """
        # Must be a top-level job
        assert not self.has_parent, (
            "Attempted to attach child notification overrides to a job other "
            "than the top-level job in the hierarchy"
        )

        # Must be a meta-job
        from .meta import MetaTemplate
        template = self.template.upcast()
        if not isinstance(template, MetaTemplate):
            raise ChildNotificationOverridesForWorkableJob()

        # Process overrides for each descendant
        for descendant_name, descendant_overrides in overrides.items():
            # Get the descendant template
            descendant_template = template.get_descendant(descendant_name)

            # If there is no descendant by that name, error
            if descendant_template is None:
                raise BadDescendantName(template, descendant_name)

            # Create the override
            NotificationOverride(
                job=self,
                name=descendant_name,
                override=descendant_overrides.to_json_string()
            ).save()

    def attach_notifications(self, actions: NotificationActions):
        """
        Sets the notifications for the job to those provided.

        :param actions:
                    The specifications of the notifications to send
                    and when.
        """
        # Check for notifications for each transition
        for transition in Transition:
            # Get the notifications to send for this transition
            notifications = actions.get_property(transition.json_property_name)

            # Attach an instance of each notification to this job
            for notification_json in notifications:
                # Get an instance of the notification
                notification_instance = create_notification_from_json(notification_json)

                # Create the association with this job
                action = NotificationAction(
                    job=self,
                    transition_index=transition.value,
                    notification=notification_instance,
                    suppress=notification_json.suppress_for_parent
                )
                action.save()

    def attach_default_notifications(self):
        """
        Attaches the server-wide default notifications to this job.
        """
        self.attach_notifications(
            core_settings.DEFAULT_META_NOTIFICATIONS
            if self.is_meta else
            core_settings.DEFAULT_WORKABLE_NOTIFICATIONS
        )

    def set_notifications_from_override(self, override: Optional[JSONNotificationOverride]):
        """
        Sets the notifications for this job, given the specified
        overrides.

        :param override:
                    The override specification.
        """
        # If there is no override, just use the default notifications
        if override is None:
            return self.attach_default_notifications()

        # If the override says to keep the defaults, attach them first
        if override.keep_default:
            self.attach_default_notifications()

        # Attach the notifications from the override
        self.attach_notifications(override.actions)

    def _perform_notifications(self, transition: Transition, **other: RawJSONElement):
        """
        Performs any notifications specified for this job, based
        on the phase transition it is going through.

        :param transition:
                    The transition the job is making.
        """
        # Get our notifications for this transition
        notification_actions = self.notification_actions.for_transition(transition)

        # Get the notification data for this transition
        notification_data: Dict[str, RawJSONElement] = self._get_notification_data(transition)
        notification_data['transition_data'] = other

        # Perform the notifications
        for notification_action in notification_actions.all():
            # Suppress if part of a workflow
            if notification_action.suppress and self.has_parent:
                continue

            notification_action.notification.upcast().perform(self, **notification_data)

    def _get_notification_data(
            self,
            transition: Transition
    ) -> RawJSONObject:
        """
        Get the format strings for formatting notification messages.

        :param transition:
                    The phase transition that the job is going through.
        :return:
                    The format keyword arguments.
        """
        # These kwargs are always present
        kwargs = dict(
            transition=transition.name.lower(),
            description=self.description,
            pk=self.pk,
            progress=self.progress_amount,
            cancelled=self.is_cancelled
        )

        # Add the node's primary key if there is one
        if self.node is not None:
            kwargs['node'] = self.node.pk

        # Add the error message if there is one
        if self.is_errored:
            kwargs['error'] = self.error_reason

        return kwargs

    # endregion
