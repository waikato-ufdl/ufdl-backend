from typing import Dict, Optional

from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

from ufdl.json.core.jobs.notification import WebSocketNotification as JSONWebSocketNotification

from wai.json.raw import RawJSONElement

from ._Notification import Notification, NotificationQuerySet
from ._Transition import Transition

class WebSocketNotificationQuerySet(NotificationQuerySet):
    """
    A query-set of web-socket notifications.
    """
    pass


class WebSocketNotification(Notification):
    """
    A specification of a web-socket notification, sends to a web-scoket for a job.
    """
    objects = WebSocketNotificationQuerySet.as_manager()

    @classmethod
    def create(cls) -> 'WebSocketNotification':
        """
        Creates an instance of this model, or returns a matching existing
        instance.

        :return:
                    The new or existing instance.
        """
        # Get the existing instance, if any
        existing = WebSocketNotification.objects.first()

        # If not, create a new instance
        if existing is None:
            existing = WebSocketNotification()
            existing.save()

        return existing

    @classmethod
    def from_json(cls, json: JSONWebSocketNotification) -> 'WebSocketNotification':
        return cls.create()

    def to_json(self) -> JSONWebSocketNotification:
        return JSONWebSocketNotification()

    def perform(self, job: 'Job', **data: RawJSONElement):
        try:
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                job.websocket_group_name,
                {
                    'type': 'transition.enact',
                    'content': data
                }
            )
        except Exception as e:
            print(f"Error sending web-socket message: {e}")


class WebSocketNotificationConsumer(JsonWebsocketConsumer):
    """
    TODO
    """
    @property
    def job_pk(self) -> int:
        return int(self.scope['url_route']['kwargs']['pk'])

    @property
    def group_name(self) -> str:
        return f"Job-{self.job_pk}"

    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # Get the job being monitored
        from .._Job import Job, LifecyclePhase
        job: Optional[Job] = Job.objects.filter(pk=self.job_pk).first()

        # If the job doesn't exist, no messages will be sent
        if job is None:
            self.close()
            return

        # If the job has no web-socket notifications, no messages will be sent
        if not any(
            isinstance(notification_action.notification.upcast(), WebSocketNotification)
            for notification_action in job.notification_actions.all()
        ):
            self.close()
            return

        self.accept()

        # Work out a proxy for the last transition
        transition = {
            LifecyclePhase.CREATED: None,
            LifecyclePhase.STARTED: Transition.PROGRESS,
            LifecyclePhase.FINISHED: Transition.FINISH,
            LifecyclePhase.ERRORED: Transition.ERROR,
            LifecyclePhase.CANCELLED: Transition.CANCEL
        }[job.lifecycle_phase]

        # If the job has just been created, no transitions have occurred
        if transition is None:
            return

        # Get the notification data for this transition
        notification_data: Dict[str, RawJSONElement] = job._get_notification_data(transition)
        notification_data['transition_data'] = {}

        # Perform the notifications
        for notification_action in job.notification_actions.for_transition(transition).all():
            # Suppress if part of a workflow
            if notification_action.suppress and job.has_parent:
                continue

            notification = notification_action.notification.upcast()

            if isinstance(notification, WebSocketNotification):
                notification.perform(job, **notification_data)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def transition_enact(self, event):
        self.send_json(event['content'])
