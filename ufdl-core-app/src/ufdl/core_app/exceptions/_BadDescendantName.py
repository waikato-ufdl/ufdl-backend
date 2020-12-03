from rest_framework import status
from rest_framework.exceptions import APIException


class BadDescendantName(APIException):
    """
    Exception for when an attempt is made to add notification overrides
    for a non-existing descendant of a meta-job.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'bad_descendant_name'

    def __init__(
            self,
            template,
            descendant_name: str
    ):
        super().__init__(
            f"Unknown descendant for job from template #{template.pk}: {descendant_name}"
        )
