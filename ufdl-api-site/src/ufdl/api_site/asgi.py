import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import django
from django.core.asgi import get_asgi_application
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')
django.setup()

from ufdl.core_app.models.jobs.notifications import WebSocketNotificationConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                re_path('v1/jobs/(?P<pk>[1-9][0-9]*)$', WebSocketNotificationConsumer.as_asgi())
            ]
        )
    ),
})
