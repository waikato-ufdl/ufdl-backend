from rest_framework import status
from rest_framework.exceptions import APIException


class JobStarted(APIException):
    """
    Exception for when a node tries to perform an action
    on a job that it has already started.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'job_started'

    def __init__(self, action: str):
        super().__init__(f"Attempted to perform the following action on a started job: {action}")
