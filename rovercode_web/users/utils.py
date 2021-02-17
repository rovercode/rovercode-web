"""Users utils."""
import json

from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import requests


# pylint: disable=abstract-method
class JwtSerializer(TokenObtainPairSerializer):
    """Custom serializer to add claims to the token."""

    @classmethod
    def get_token(cls, user):
        """Get the token for the user."""
        token = super().get_token(user)
        token['show_guide'] = user.show_guide
        token['username'] = user.username

        user_id = token['user_id']
        auth_jwt = str(token)
        subscription_service = settings.SUBSCRIPTION_SERVICE_HOST
        try:
            response = requests.get(
                f'{subscription_service}/api/v1/customer/{user_id}/',
                headers={'Authorization': f'JWT {auth_jwt}'}
            )
            data = response.json()
            token['tier'] = int(data['subscription']['plan'])
        except (
            json.decoder.JSONDecodeError,
            KeyError,
            ValueError,
            requests.exceptions.ConnectionError
        ):
            # If unable to determine tier, set to lowest
            token['tier'] = 1

        return token
