"""User signal handlers."""
import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rovercode_web.users.utils import JwtObtainPairSerializer

import requests

LOGGER = logging.getLogger(__name__)


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='new_user')
def create_new_user(sender, instance, created, **kwargs):
    """Handle new user being created."""
    if not created:
        return

    token = JwtObtainPairSerializer.get_token(instance)
    token['admin'] = True
    auth_jwt = str(token)

    response = requests.post(
        f'{settings.SUBSCRIPTION_SERVICE_HOST}/api/v1/customer/', json={
            "id": instance.id,
        },
        headers={'Authorization': f'JWT {auth_jwt}'}
    )

    if response.status_code != 200:
        LOGGER.error(
            'Error %s contacting subscription service', response.status_code)
