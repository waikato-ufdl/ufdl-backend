from django.db import models

from ufdl.json.core.jobs.notification import PrintNotification as JSONPrintNotification

from ._Notification import Notification, NotificationQuerySet


class PrintNotificationQuerySet(NotificationQuerySet):
    """
    A query-set of print notifications.
    """
    pass


class PrintNotification(Notification):
    """
    A specification of a print notification, which prints to
    standard output.
    """
    # The message to print
    message = models.TextField()

    objects = PrintNotificationQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each notification specification is unique
            models.UniqueConstraint(
                name="unique_print_notifications",
                fields=["message"]
            )
        ]

    @classmethod
    def create(cls, message: str) -> 'PrintNotification':
        """
        Creates an instance of this model, or returns a matching existing
        instance.

        :param message:
                    The message to print.
        :return:
                    The new or existing instance.
        """
        # Get the existing instance, if any
        existing = PrintNotification.objects.filter(message=message).first()

        # If not, create a new instance
        if existing is None:
            existing = PrintNotification(message=message)
            existing.save()

        return existing

    @classmethod
    def from_json(cls, json: JSONPrintNotification) -> 'PrintNotification':
        return cls.create(json.message)

    def to_json(self) -> JSONPrintNotification:
        return JSONPrintNotification(message=self.message)
