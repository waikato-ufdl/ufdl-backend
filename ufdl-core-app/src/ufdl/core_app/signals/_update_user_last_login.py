from django.dispatch import receiver
from django.utils.timezone import now

from ..models import User
from ._all_requests import all_requests


@receiver(all_requests, dispatch_uid='update_user_last_login')
def update_user_last_login(sender, **kwargs):
    """
    Updates the last-login field of the user.

    :param sender:
    :param kwargs:
    :return:
    """
    # Get the request from the keyword arguments
    request = kwargs['request']

    # Update the last-login field of the user if it is one
    user = request.user
    if isinstance(user, User):
        user.last_login = now()
        user.save(update_fields=["last_login"])
