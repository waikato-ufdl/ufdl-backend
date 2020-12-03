from rest_framework import status
from rest_framework.exceptions import APIException


class ChildNotificationOverridesForWorkableJob(APIException):
    """
    Exception for when an attempt is made to add notification overrides
    for children of a job that does not have children.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'child_notification_overrides_for_workable_job'

    def __init__(self):
        super().__init__(
            f"Attempted an add child notification overrides to a non-meta-job"
        )
