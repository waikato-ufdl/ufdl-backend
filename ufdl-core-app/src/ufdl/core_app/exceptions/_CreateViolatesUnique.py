from rest_framework import status
from rest_framework.exceptions import APIException


class CreateViolatesUnique(APIException):
    """
    Exception for when an attempt is made to create a model
    that violates a unique constraint.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'create_violates_unique'

