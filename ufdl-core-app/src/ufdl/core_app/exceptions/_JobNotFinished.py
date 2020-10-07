from rest_framework import status
from rest_framework.exceptions import APIException


class JobNotFinished(APIException):
    """
    Exception for when a user tries to perform an action
    on a job that has not yet finished.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'job_not_finished'

    def __init__(self, action: str):
        super().__init__(f"Attempted to perform the following action on an unfinished job: {action}")
