from rest_framework import status
from rest_framework.exceptions import APIException


class JobFinished(APIException):
    """
    Exception for when a node tries to perform an action
    on a job that has already finished.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'job_finished'

    def __init__(self, action: str):
        super().__init__(f"Attempted to perform the following action on a finished job: {action}")
