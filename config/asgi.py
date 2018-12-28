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
from middleware.channels_jwt_middleware import ChannelsJwtMiddleware
from middleware.channels_oauth2_middleware import ChannelsOAuth2Middleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(ChannelsJwtMiddleware(ChannelsOAuth2Middleware(AuthMiddlewareStack(
        URLRouter(
            realtime.routing.websocket_urlpatterns
        )
    )))),
})
