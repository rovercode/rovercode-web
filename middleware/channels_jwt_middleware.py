"""JWT auth middleware for Django Channels."""
import logging
from django.contrib.auth.models import AnonymousUser

from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
LOGGER = logging.getLogger(__name__)


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
        if scope.get('user') and scope['user'] != AnonymousUser:
            # We already have an authenticated user
            return self.inner(scope)

        if "method" not in scope:
            scope['method'] = "FAKE"

        cookies = scope.get("cookies")
        if not cookies:
            return self.inner(scope)

        jwt_cookie = cookies.get("auth_jwt")
        if not jwt_cookie:
            return self.inner(scope)

        data = {'token': jwt_cookie}
        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
        except ValidationError as err:
            LOGGER.warning("Token present, but couldn't be verified: %s", err)
            return self.inner(scope)

        user = valid_data.get("user")
        if not user:
            return self.inner(scope)

        scope['user'] = user
        return self.inner(scope)
