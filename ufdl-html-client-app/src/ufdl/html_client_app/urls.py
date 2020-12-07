import os

from django.urls import re_path
from django.views.static import serve

from .settings import html_client_settings

# The root directory of the static site files
ROOT = f'{os.path.split(__file__)[0]}/static/build'

# The landing page of the client
LANDING_PAGE = 'index.html'


# The final set of URLs routed by this app
urlpatterns = []
if html_client_settings.SERVE_CLIENT:
    urlpatterns += [
        re_path(r'^$', serve, kwargs={'document_root': ROOT, 'path': LANDING_PAGE}),
        re_path(r'^(?P<path>.+)$', serve, kwargs={'document_root': ROOT})
    ]

# Default namespace for the views
app_name = "ufdl-html-client-app"
