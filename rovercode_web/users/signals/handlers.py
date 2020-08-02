"""User signal handlers."""
import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.settings import api_settings

import requests

LOGGER = logging.getLogger(__name__)

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='new_user')
def create_new_user(sender, instance, created, **kwargs):
    """Handle new user being created."""
    if not created:
        return

    payload = jwt_payload_handler(instance)
    payload['admin'] = True
    auth_jwt = jwt_encode_handler(payload)

    response = requests.post(
        f'{settings.SUBSCRIPTION_SERVICE_HOST}/api/v1/customer/', json={
            "id": instance.id,
        },
        headers={'Authorization': f'JWT {auth_jwt}'}
    )

    if response.status_code != 200:
        LOGGER.error(
            'Error %s contacting subscription service', response.status_code)
