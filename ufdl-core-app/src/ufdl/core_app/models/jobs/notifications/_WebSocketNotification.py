from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

from ufdl.json.core.jobs.notification import WebSocketNotification as JSONWebSocketNotification

from wai.json.raw import RawJSONElement

from ._Notification import Notification, NotificationQuerySet


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
    def connect(self):
        job_pk = self.scope['url_route']['kwargs']['pk']
        self.group_name = f"Job-{job_pk}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def transition_enact(self, event):
        self.send_json(event['content'])
