from rest_framework import status
from rest_framework.exceptions import APIException


class BadName(APIException):
    """
    Exception for when a name specified by the user is
    unusable for some reason.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_name'

    def __init__(self, name: str, reason: str):
        super().__init__(f"Bad name '{name}': {reason}")
