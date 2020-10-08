from rest_framework import status
from rest_framework.exceptions import APIException


class JobAcquired(APIException):
    """
    Exception for when a node tries to acquire a job
    that has already been claimed.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'job_acquired'

    def __init__(self):
        super().__init__(f"Attempted to acquire job that has already been acquired")
