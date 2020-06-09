from logging import Logger, getLogger

from ._BackendLoggingHandler import BackendLoggingHandler

# The UFDL backend logger
__logger: Logger = getLogger("ufdl")
__logger.addHandler(BackendLoggingHandler())
__logger.setLevel(1)


def get_backend_logger() -> Logger:
    """
    Gets the logger for the UFDL backend.

    :return:    The logger.
    """
    return __logger
