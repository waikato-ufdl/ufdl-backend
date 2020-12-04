from typing import Optional

from rest_framework import status
from rest_framework.exceptions import APIException


class BadArgumentValue(APIException):
    """
    Exception for when the argument supplied is not
    an allowed value.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_argument_value'

    def __init__(
            self,
            action_name: str,
            parameter_name: str,
            value: str,
            allowed_values: Optional[str] = None,
            reason: Optional[str] = None,
    ):
        # Format the allowed values
        allowed_values = (
            f", options: {allowed_values}"
            if allowed_values is not None else
            ""
        )

        # Format the reason
        reason = (
            ""
            if reason is None else
            f"\n{reason}"
        )

        super().__init__(
            f"Bad value for {action_name} parameter '{parameter_name}': {value}"
            f"{allowed_values}"
            f"{reason}"
        )
