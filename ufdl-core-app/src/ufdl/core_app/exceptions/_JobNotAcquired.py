from rest_framework import status
from rest_framework.exceptions import APIException


class JobNotAcquired(APIException):
    """
    Exception for when a node tries to release a job
    that it has not acquired.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'job_not_acquired'

    def __init__(self, job):
        super().__init__(f"Attempted to release job #{job.pk} that has not been acquired")
