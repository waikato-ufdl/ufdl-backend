from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidJobInput(APIException):
    """
    Exception for when a job is created with invalid input.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'invalid_job_input'

    def __init__(self, reason: str):
        super().__init__(reason)
