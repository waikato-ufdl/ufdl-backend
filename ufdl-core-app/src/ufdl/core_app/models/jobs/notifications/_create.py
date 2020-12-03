from typing import Type

from ufdl.json.core.jobs.notification import *

from ._EmailNotification import EmailNotification as EmailNotificationModel
from ._Notification import Notification as NotificationModel
from ._PrintNotification import PrintNotification as PrintNotificationModel


def create_notification_from_json(json: NotificationUnionType) -> NotificationModel:
    """
    Creates a notification in the database based on the provided
    JSON specification.

    :param json:
                The JSON specification of the notification.
    :return:
                The instance created in the database.
    """
    # Get the model corresponding to this JSON type
    model: Type[NotificationModel] = (
        PrintNotificationModel
        if isinstance(json, PrintNotification) else
        EmailNotificationModel
        if isinstance(json, EmailNotification) else
        None
    )

    # Must have a known model for the JSON type
    if model is None:
        raise Exception(f"Unknown json type: {type(json).__qualname__}")

    return model.from_json(json)
