"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.local'

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

django.setup()
# if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
#     application = Sentry(application)

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import realtime.routing
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            realtime.routing.websocket_urlpatterns
        )
    ),
})
