from django.db import models

from ....apps import UFDLCoreAppConfig
from ...mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class NotificationOverrideQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of notification overrides.
    """
    def with_name(self, name: str) -> 'NotificationOverrideQuerySet':
        """
        Filters the overrides to those with the given name.

        :param name:
                    The name to find.
        :return:
                    The filtered query-set.
        """
        return self.filter(name=name)


class NotificationOverride(DeleteOnNoRemainingReferencesOnlyModel):
    """
    Tells a job how to override the notifications of any sub-jobs
    it might create. Only held by the outermost parent job.
    """
    # The parent job, the children of which these overrides refer to
    job = models.ForeignKey(
        f"{UFDLCoreAppConfig.label}.Job",
        on_delete=models.DO_NOTHING,
        related_name="notification_overrides"
    )

    # The name of the child job the overrides correspond to
    name = models.TextField()

    # The override JSON text
    override = models.TextField()

    objects = NotificationOverrideQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each child only has one override
            models.UniqueConstraint(
                name="unique_child_notification_overrides",
                fields=["job", "name"]
            )
        ]