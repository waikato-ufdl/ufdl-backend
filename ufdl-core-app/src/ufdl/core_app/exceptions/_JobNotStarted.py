from rest_framework import status
from rest_framework.exceptions import APIException


class JobNotStarted(APIException):
    """
    Exception for when a node tries to perform an action
    on a job that it hasn't officially started yet.
    """
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_code = 'job_not_started'

    def __init__(self, action: str):
        super().__init__(f"Attempted to perform the following action on an un-started job: {action}")
