"""OAuth2 middleware for Django Channels."""
from django.contrib.auth.models import AnonymousUser

from channels.http import AsgiRequest
from oauth2_provider.oauth2_backends import get_oauthlib_core


class ChannelsOAuth2Middleware:
    """
    OAuth2 middleware class for Channels.

    Credit:
    https://gist.github.com/stuartaccent/34852c8ccd5828bb2cc81dddb68e6538

    Works in the same way as
    `oauth2_provider.contrib.rest_framework.OAuth2Authentication`
    but for django channels 2. Passes the scope into an AsgiRequest
    header, and then passes it onto oauth2_provider to validate.
    Usage:
    application = ProtocolTypeRouter({
        ...
        "websocket": OAuth2Middleware(
            URLRouter([
                ...
            ]),
        ),
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
        def authenticate(request):
            """
            Authenticate the request.

            Returns a tuple containing the user and their access token.
            If it's not valid then AnonymousUser is returned.
            """
            oauthlib_core = get_oauthlib_core()
            valid, r = oauthlib_core.verify_request(request, scopes=[])
            if valid:
                return r.user, r.access_token
            return AnonymousUser, None

        if scope.get('user') and scope['user'] != AnonymousUser:
            # We already have an authenticated user
            return self.inner(scope)

        if "method" not in scope:
            scope['method'] = "FAKE"

        request = AsgiRequest(scope, b"")

        if request.META.get("HTTP_AUTHORIZATION"):
            user, _ = authenticate(request)
            scope['user'] = user
        else:
            scope['user'] = AnonymousUser

        return self.inner(scope)
