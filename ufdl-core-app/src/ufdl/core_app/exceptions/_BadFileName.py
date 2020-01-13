from rest_framework import status
from rest_framework.exceptions import APIException


class BadFileName(APIException):
    """
    Exception for when a filename specified by the user is
    unusable for some reason.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_file_name'

    def __init__(self, filename: str, reason: str):
        super().__init__(f"Bad filename '{filename}': {reason}")
