from rest_framework import status
from rest_framework.exceptions import APIException


class NotServerResidentType(APIException):
    """
    Error for when asked to list values of a type that isn't a server-type.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'not_server_resident_type'

    def __init__(self, type_string: str):
        super().__init__(f"{type_string} is not a server-resident type")
