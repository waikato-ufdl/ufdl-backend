from rest_framework import status
from rest_framework.exceptions import APIException


class MergeDisallowed(APIException):
    """
    Exception for when a merge cannot be performed.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'merge_disallowed'

    def __init__(self, reason: str):
        super().__init__(
            f"Cannot perform merge:\n"
            f"{reason}"
        )
