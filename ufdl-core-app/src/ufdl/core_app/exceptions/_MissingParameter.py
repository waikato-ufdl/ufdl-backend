from rest_framework import status
from rest_framework.exceptions import APIException


class MissingParameter(APIException):
    """
    Exception for when a required parameter is not specified.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'missing_parameter'

    def __init__(self, name: str):
        super().__init__(f"Required parameter '{name}' is missing")
