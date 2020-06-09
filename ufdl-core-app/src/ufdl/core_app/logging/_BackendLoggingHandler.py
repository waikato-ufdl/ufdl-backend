from logging import Handler, LogRecord

from ..models import LogEntry


class BackendLoggingHandler(Handler):
    """
    Handler which inserts log records into the database.
    """
    def emit(self, record: LogRecord):
        # Create an entry in the log table for the record
        log_entry = LogEntry(level=record.levelno,
                             is_internal=True,
                             message=record.getMessage())

        # Save it
        log_entry.save()
