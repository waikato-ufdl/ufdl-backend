import os

from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

import django
from django.urls import re_path

from ufdl.core_app.models.jobs.notifications import WebSocketNotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')
django.setup()

application = ProtocolTypeRouter({
    'http': AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path('ws/job/(?P<pk>[1-9][0-9]*)$', WebSocketNotificationConsumer.as_asgi())
            ]
        )
    ),
})
