from django.db import models

from ....apps import UFDLCoreAppConfig
from ...mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet
from ._Transition import Transition


class NotificationActionQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of notification actions.
    """
    def for_transition(self, transition: Transition):
        """
        Filters the query-set to those actions that correspond
        to a particular phase transition.

        :param transition:
                    The transition.
        :return:
                    The filtered query-set.
        """
        return self.filter(transition_index=transition.value)


class NotificationAction(DeleteOnNoRemainingReferencesOnlyModel):
    """
    An notification to send out when a job goes through a phase transition.
    """
    # The job that is monitored for phase transitions.
    job = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Job",
        on_delete=models.DO_NOTHING,
        related_name="notification_actions"
    )

    # The index of the phase transition that this action is for
    transition_index = models.PositiveSmallIntegerField(
        choices=tuple(
            (transition.value, transition.name)
            for transition in Transition
        )
    )

    # The notification that is monitored for phase transitions.
    notification = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Notification",
        on_delete=models.DO_NOTHING,
        related_name="+"
    )

    # Whether this notification is suppressed when the job is part of a workflow
    suppress = models.BooleanField()

    objects = NotificationActionQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each notification only occurs once
            models.UniqueConstraint(
                name="unique_notifications",
                fields=["job", "transition_index", "notification"]
            )
        ]

    @property
    def transition(self) -> Transition:
        """
        The phase transition that this action is for.
        """
        return Transition(self.transition_index)
