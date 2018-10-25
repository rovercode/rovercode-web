from django.contrib.auth.models import AnonymousUser

from channels.http import AsgiRequest
from oauth2_provider.oauth2_backends import get_oauthlib_core


class ChannelsOAuth2Middleware:
    """
    Credit: https://gist.github.com/stuartaccent/34852c8ccd5828bb2cc81dddb68e6538

    Works in the same way as `oauth2_provider.contrib.rest_framework.OAuth2Authentication`
    but for Django Channels 2.

    Passes the scope into an AsgiRequest and adds the bearer token as an authorization
    header. Finally passes it onto oauth2_provider to validate.

    Usage:

    application = ProtocolTypeRouter({
        ...
        "websocket": ChannelsOAuth2Middleware(
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
        self.inner = inner

    def __call__(self, scope):
        if "method" not in scope:
            scope['method'] = "FAKE"

        request = AsgiRequest(scope, b"")

        auth_token = request.GET.get('token', None)

        if auth_token:
            # add the bearer token to the request and validate
            request.META["HTTP_AUTHORIZATION"] = "Bearer {}".format(auth_token)
            user, token = self.authenticate(request)
            scope['user'] = user
        else:
            # no token in request to set user to anonymous
            scope['user'] = AnonymousUser

        return self.inner(scope)

    def authenticate(self, request):
        """
        Authenticates the request and returns a tuple containing the user and their access token,
        if not valid then AnonymousUser is returned.
        """

        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])
        if valid:
            return r.user, r.access_token
        else:
            return AnonymousUser, None
