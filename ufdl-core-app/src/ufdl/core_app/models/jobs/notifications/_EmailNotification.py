from typing import List, Dict

from django.core.mail import EmailMessage
from django.db import models

from ufdl.json.core.jobs.notification import EmailNotification as JSONEmailNotification

from wai.json.object import Absent
from wai.json.raw import RawJSONElement, is_raw_json_primitive

from ._Notification import Notification, NotificationQuerySet


class EmailNotificationQuerySet(NotificationQuerySet):
    """
    A query-set of email notifications.
    """
    pass


class EmailNotification(Notification):
    """
    A specification of an email notification.
    """
    # The email subject
    subject = models.TextField()

    # The body of the email
    body = models.TextField()

    # The recipients of the email
    to = models.TextField(null=True)

    # The copied recipients of the email
    cc = models.TextField(null=True)

    # The blind-copied recipients of the email
    bcc = models.TextField(null=True)

    objects = EmailNotificationQuerySet.as_manager()

    class Meta:
        constraints = [
            # Ensure that each notification specification is unique
            models.UniqueConstraint(
                name="unique_email_notifications",
                fields=["subject", "body", "to", "cc", "bcc"]
            )
        ]

    @classmethod
    def create(
            cls,
            subject: str,
            body: str,
            to: List[str],
            cc: List[str],
            bcc: List[str]
    ) -> 'EmailNotification':
        """
        Creates an instance of this model, or returns a matching existing
        instance.

        :param subject:
                    The email subject.
        :param body:
                    The email body.
        :param to:
                    The list of email recipients.
        :param cc:
                    The list of copied recipients.
        :param bcc:
                    The list of blind-copied recipients.
        :return:
                    The new or existing instance.
        """
        # Format the arguments for the constructor
        kwargs = dict(
            subject=subject,
            body=body,
            to="\n".join(to) if len(to) > 0 else None,
            cc="\n".join(cc) if len(cc) > 0 else None,
            bcc="\n".join(bcc) if len(bcc) > 0 else None
        )

        # Check if an equivalent instance already exists
        existing = EmailNotification.objects.filter(**kwargs).first()

        # If not, create a new instance
        if existing is None:
            existing = EmailNotification(**kwargs)
            existing.save()

        return existing

    @classmethod
    def from_json(cls, json: JSONEmailNotification) -> 'EmailNotification':
        return cls.create(
            json.subject,
            json.body,
            json.to if json.to is not Absent else [],
            json.cc if json.cc is not Absent else [],
            json.bcc if json.bcc is not Absent else [],
        )

    def to_json(self) -> JSONEmailNotification:
        return JSONEmailNotification(
            subject=self.subject,
            body=self.body,
            to=self.to.split("\n") if self.to is not None else Absent,
            cc=self.cc.split("\n") if self.cc is not None else Absent,
            bcc=self.bcc.split("\n") if self.bcc is not None else Absent,
        )

    def perform(self, job: 'Job', **data: RawJSONElement):
        # Stringify the data
        all_data_str: Dict[str, str] = {key: str(value) for key, value in data.items()}
        primitive_data_str: Dict[str, str] = {
            key: str(value) for key, value in data.items()
            if is_raw_json_primitive(value)
        }

        # Create and format the email to send
        message = EmailMessage(
            subject=self.subject.format(**primitive_data_str),
            body=self.body.format(**all_data_str),
            to=(
                self.to.split("\n")
                if self.to is not None else
                [job.creator.email]
            ),
            cc=(
                self.cc.split("\n")
                if self.cc is not None else
                None
            ),
            bcc=(
                self.bcc.split("\n")
                if self.bcc is not None else
                None
            )
        )

        # Send the email
        try:
            message.send()
        except Exception as e:
            print(f"Error sending email notification: {e}")
