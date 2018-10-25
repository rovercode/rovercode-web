from django.contrib.auth.models import AnonymousUser

from rovercode_web.users.models import User

MOCK_USER_ID = 1


class MockAuthMiddleware:
    """
    Note: Puts a dummy user in the scope

    Usage:

    application = ProtocolTypeRouter({
        ...
        "websocket": MockAuthMiddleware(
            URLRouter([
                ...
            ]),
        )),
    })

    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        scope['user'] = User(id=MOCK_USER_ID)
        return self.inner(scope)
