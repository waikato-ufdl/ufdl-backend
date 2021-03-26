from rest_framework import status
from rest_framework.exceptions import APIException


class IllegalPhaseTransition(APIException):
    """
    Exception for when an attempt is made to perform a phase transition
    that doesn't make sense for a job.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'illegal_phase_transition'

    def __init__(
            self,
            job,
            transition: str,
            reason: str
    ):
        job_type = (
            "meta-job"
            if job.is_meta else
            "workable job"
        )

        super().__init__(
            f"Attempted an illegal phase-transition "
            f"on {job_type} {job.pk} in phase {job.lifecycle_phase}: {transition}\n"
            f"{reason}."
        )
