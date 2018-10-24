"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import realtime.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(AuthMiddlewareStack(
        URLRouter(
            realtime.routing.websocket_urlpatterns
        )
    )),
})
