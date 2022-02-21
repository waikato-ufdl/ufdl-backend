from rest_framework import status
from rest_framework.exceptions import APIException


class TypeIsAbstract(APIException):
    """
    Error for when asked to use an abstract type as a concrete type.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'type_is_abstract'

    def __init__(self, type_string: str):
        super().__init__(f"{type_string} is abstract")
