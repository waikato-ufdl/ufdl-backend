from rest_framework import status
from rest_framework.exceptions import APIException


class BadJobTemplate(APIException):
    """
    Exception for when an imported job template is unable to
    be created.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_job_template'

    def __init__(self, reason: str):
        super().__init__(f"Bad job template: {reason}")
