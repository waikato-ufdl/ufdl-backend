from rest_framework import status
from rest_framework.exceptions import APIException


class BadNodeID(APIException):
    """
    Exception for when a user adds a node-id header to a
    request that can't be resolved to a node.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bad_node_id'

    def __init__(self, node_id: str, reason: str):
        super().__init__(f"Bad Node-Id header '{node_id}': {reason}")
