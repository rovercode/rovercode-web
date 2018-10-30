"""Middleware for Channels testing that puts a user in the context."""
from rovercode_web.users.models import User

MOCK_USER_ID = 1


class MockAuthMiddleware:
    """
    Puts a dummy user in the scope.

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
        """Initialize the middleware."""
        self.inner = inner

    def __call__(self, scope):
        """Call the middleware."""
        scope['user'] = User(id=MOCK_USER_ID)
        return self.inner(scope)
