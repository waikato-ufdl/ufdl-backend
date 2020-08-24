from django.dispatch import receiver
from django.utils.timezone import now

from ..models.nodes import Node
from ._all_requests import all_requests


@receiver(all_requests, dispatch_uid='update_node_last_seen')
def update_node_last_seen(sender, **kwargs):
    """
    Updates the last-seen field of the user's node.

    :param sender:  The sender of the signal (unused).
    :param kwargs:  The signal arguments (should include a 'request' keyword).
    """
    # Get the request from the keyword arguments
    request = kwargs['request']

    # Update the last-seen field of the user's node if it is one
    node = Node.from_request(request)
    if node is not None:
        node.last_seen = now()
        node.save(update_fields=["last_seen"])
