from typing import Type

from django.db.models import Model

from rest_framework import status
from rest_framework.exceptions import APIException


class BadModelType(APIException):
    """
    Exception for when the target model of an operation is not
    the type expected by the operation. This usually indicates
    a problem with the backend code.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'bad_model_type'

    def __init__(self,
                 expected_model_type: Type[Model],
                 actual_model_type: Type[Model]):
        super().__init__(f"Model should be of type '{expected_model_type.__name__}' but "
                         f"was of type '{actual_model_type.__name__}'")
