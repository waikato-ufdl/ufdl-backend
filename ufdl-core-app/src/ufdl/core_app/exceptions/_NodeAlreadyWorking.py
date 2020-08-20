from rest_framework import status
from rest_framework.exceptions import APIException


class NodeAlreadyWorking(APIException):
    """
    Exception for when a node tries to start a job when it
    hasn't finished its last one.
    """
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = 'node_already_working'

    def __init__(self):
        super().__init__(f"Attempted to start a job with another already in progress")
