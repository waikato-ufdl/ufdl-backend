from rest_framework import status
from rest_framework.exceptions import APIException

from ufdl.jobtypes.error import TypeParsingException


class CouldntParseType(APIException):
    """
    Error for when type-parsing fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'couldnt_parse_type'

    def __init__(self, error: TypeParsingException):
        super().__init__(f"{error}")
