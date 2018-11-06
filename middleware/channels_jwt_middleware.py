"""JWT auth middleware for Django Channels."""
from django.contrib.auth.models import AnonymousUser

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


class ChannelsJwtMiddleware:
    """
    Note: Relies of SessionMiddlewareStack for easy cookie access.

    Usage:

    from channels.sessions import SessionMiddlewareStack
    application = ProtocolTypeRouter({
        ...
        "websocket": SessionMiddlewareStack(ChannelsJwtMiddleware)(
            URLRouter([
                ...
            ]),
        )),
    })

    Consumer:

    class MyConsumer(AsyncJsonWebsocketConsumer):

        async def connect(self):
            if self.scope["user"].is_anonymous:
                await self.close()
            else:
                await self.accept()
    """

    def __init__(self, inner):
        """Init the middleware."""
        self.inner = inner

    def __call__(self, scope):
        """Call the middleware."""
        if "method" not in scope:
            scope['method'] = "FAKE"

        cookies = scope.get("cookies")
        if not cookies:
            scope['user'] = AnonymousUser
            return self.inner(scope)

        data = {'token': cookies.get("auth_jwt")}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        if not user:
            scope['user'] = AnonymousUser
            return self.inner(scope)

        scope['user'] = user
        return self.inner(scope)
