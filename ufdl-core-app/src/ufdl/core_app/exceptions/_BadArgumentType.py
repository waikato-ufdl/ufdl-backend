from rest_framework import status
from rest_framework.exceptions import APIException


class BadArgumentType(APIException):
    """
    Exception for when the argument supplied is not of the
    type expected by the action.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_argument_type'

    def __init__(self, action_name: str,
                 parameter_name: str,
                 expected_type: str,
                 actual_type: str):
        super().__init__(f"The type passed to {action_name} parameter '{parameter_name}' "
                         f"should be '{expected_type}', but received '{actual_type}'")
