"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import realtime.routing
import support.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            realtime.routing.websocket_urlpatterns +
            support.routing.websocket_urlpatterns
        )
    ),
})

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(application)
