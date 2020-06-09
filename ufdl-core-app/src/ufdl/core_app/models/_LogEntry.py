from django.db import models


class LogEntryQuerySet(models.QuerySet):
    """
    Custom query-set for working with groups of log entries.
    """
    pass


class LogEntry(models.Model):
    """
    An entry in the interaction log. Can be generated internally by the
    backend or supplied by a client.
    """
    # The time the log entry was created
    creation_time = models.DateTimeField(auto_now_add=True,
                                         editable=False)

    # The severity level of the logged event
    level = models.PositiveSmallIntegerField()

    # Whether the log record was generated internally, or provided via a client
    is_internal = models.BooleanField(default=False, editable=False)

    # The message content of the log entry
    message = models.TextField()

    objects = LogEntryQuerySet.as_manager()
