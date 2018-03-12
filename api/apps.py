"""API apps."""
from django.apps import AppConfig
from django.dispatch import receiver
from oauth2_provider.signals import app_authorized


@receiver(app_authorized)
def handle_app_authorized(sender, request, token, **kwargs):
    """Attach the application's user to the token.

    When using `client_credentials`, there isn't a user attached to an access
    token. This causes Django Rest Framework to fail to authorize when using
    the provided access token. Connecting the application's user to the token
    means that any requests made using the access token will be made as the
    user.
    """
    token.user = token.application.user
    token.save()


class ApiConfig(AppConfig):
    """Configuration for the API."""

    name = 'api'
