from rest_framework import status
from rest_framework.exceptions import APIException

from ..util import QueryParameters, QueryParameterValue


class PermissionsUndefined(APIException):
    """
    Exception for when an end-point is accessed but permissibility
    is undefined.
    """
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_code = 'permissions_undefined'

    def __init__(self, action: str):
        super().__init__(f"No permissions defined for action '{action}'")
