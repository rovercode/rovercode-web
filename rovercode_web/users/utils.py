"""Users utils."""
import json

from django.conf import settings
from rest_framework_jwt.utils import jwt_payload_handler as \
    base_jwt_payload_handler
from rest_framework_jwt.settings import api_settings

import requests

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_payload_handler(user):
    """Populate JWT with user data."""
    payload = base_jwt_payload_handler(user)
    payload['show_guide'] = user.show_guide

    user_id = payload['user_id']
    auth_jwt = jwt_encode_handler(payload)
    try:
        response = requests.get(
            f'{settings.SUBSCRIPTION_SERVICE_HOST}/api/v1/customer/{user_id}/',
            headers={'Authorization': f'JWT {auth_jwt}'}
        )
        data = response.json()
        payload['tier'] = int(data['subscription']['plan'])
    except (
        json.decoder.JSONDecodeError,
        KeyError,
        ValueError,
        requests.exceptions.ConnectionError
    ):
        # If unable to determine tier, set to lowest
        payload['tier'] = 1

    return payload
