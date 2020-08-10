from django.dispatch import receiver
from django.utils.timezone import now

from ..models import User
from ._all_requests import all_requests


@receiver(all_requests, dispatch_uid='update_node_last_seen')
def update_node_last_seen(sender, **kwargs):
    """
    Updates the last-seen field of the user's node.

    :param sender:
    :param kwargs:
    :return:
    """
    # Get the request from the keyword arguments
    request = kwargs['request']

    # Update the last-seen field of the user's node if it is one
    user = request.user
    if isinstance(user, User):
        node = user.node
        if node is not None:
            node.last_seen = now()
            node.save(update_fields=["last_seen"])
