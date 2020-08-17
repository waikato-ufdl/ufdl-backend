from rest_framework import status
from rest_framework.exceptions import APIException


class BadSource(APIException):
    """
    Exception for when a lazily-loaded data source can't
    be accessed for some reason
    """
    status_code = status.HTTP_417_EXPECTATION_FAILED
    default_code = 'bad_source'

    def __init__(self, source: str, reason: str):
        super().__init__(f"Bad source '{source}': {reason}")
