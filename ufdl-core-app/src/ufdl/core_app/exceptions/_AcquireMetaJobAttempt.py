from rest_framework import status
from rest_framework.exceptions import APIException


class AcquireMetaJobAttempt(APIException):
    """
    Exception for when a worker-node attempts to acquire
    a meta-job.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'acquire_meta_job_attempt'

    def __init__(self):
        super().__init__(
            f"Meta-jobs cannot be acquired by worker nodes"
        )
