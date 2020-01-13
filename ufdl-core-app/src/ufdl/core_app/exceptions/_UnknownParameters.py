from typing import Dict

from rest_framework import status
from rest_framework.exceptions import APIException


class UnknownParameters(APIException):
    """
    Exception for when a parameter to an end-point is
    given erroneously (for whatever reason).

    See https://softwareengineering.stackexchange.com/questions/329229/should-i-return-an-http-400-bad-request-status-if-a-parameter-is-syntactically
    """
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_code = 'unknown_parameters'

    def __init__(self, parameters: Dict[str, str]):
        super().__init__("Unknown parameters: " + ", ".join(f"{parameter}={value}"
                                                            for parameter, value in parameters.items()))
