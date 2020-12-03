from ufdl.json.core.jobs.notification import Notification as JSONNotification

from ...mixins import DeleteOnNoRemainingReferencesOnlyModel, DeleteOnNoRemainingReferencesOnlyQuerySet


class NotificationQuerySet(DeleteOnNoRemainingReferencesOnlyQuerySet):
    """
    A query-set of notifications.
    """
    pass


class Notification(DeleteOnNoRemainingReferencesOnlyModel):
    """
    A specification of a notification. Has no properties of its own,
    is just a base table grouping all types of transition together.
    """
    objects = NotificationQuerySet.as_manager()

    def upcast(self) -> 'Notification':
        """
        Up-casts this notification into its specialised sub-type.

        :return:
                    The specialised sub-type.
        """
        # If already specialised, just return ourselves
        if type(self) is not Notification:
            return self

        # Try each of the different specialisations
        for name in (
            "emailnotification",
            "printnotification"
        ):
            if hasattr(self, name):
                return getattr(self, name)

        # Raise an error if we failed
        raise Exception(f"Couldn't upcast notification {self}")

    @classmethod
    def from_json(cls, json: JSONNotification) -> 'Notification':
        """
        Creates an instance of this class from a JSON specification.

        :param json:
                    The JSON specification.
        :return:
                    The instance.
        """
        raise NotImplementedError(cls.from_json.__qualname__)

    def to_json(self) -> JSONNotification:
        """
        Gets a JSON representation of this notification.

        :return:
                    The JSON representation.
        """
        raise NotImplementedError(self.to_json.__qualname__)
