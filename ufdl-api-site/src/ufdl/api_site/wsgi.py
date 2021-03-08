"""
WSGI config for ufdl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ufdl.api_site.settings')

application = ProtocolTypeRouter({
    'http': get_wsgi_application()
})
