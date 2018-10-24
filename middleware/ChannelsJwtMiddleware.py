from django.contrib.auth.models import AnonymousUser

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

class ChannelsJwtMiddleware:
    """
    Note: Relies of SessionMiddlewareStack for easy cookie access

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
        self.inner = inner

    def __call__(self, scope):
        if "method" not in scope:
            scope['method'] = "FAKE"

        data = {'token': scope["cookies"]["auth_jwt"]}
        if not data:
            scope['user'] = AnonymousUser
        else:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            if not user:
                scope['user'] = AnonymousUser
            else:
                scope['user'] = user

        return self.inner(scope)
