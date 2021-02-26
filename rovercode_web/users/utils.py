"""Users utils."""
import json

from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

import requests


class BaseJwtSerializer:
    """Base JWT serializer to customize claims."""

    @staticmethod
    def get_user_tier(user_id, auth_jwt):
        """Get the user's tier for the subscription service."""
        subscription_service = settings.SUBSCRIPTION_SERVICE_HOST
        try:
            response = requests.get(
                f'{subscription_service}/api/v1/customer/{user_id}/',
                headers={'Authorization': f'JWT {auth_jwt}'}
            )
            data = response.json()
            return int(data['subscription']['plan'])
        except (
            json.decoder.JSONDecodeError,
            KeyError,
            ValueError,
            requests.exceptions.ConnectionError
        ):
            # If unable to determine tier, set to lowest
            return 1


# pylint: disable=abstract-method
class JwtObtainPairSerializer(BaseJwtSerializer, TokenObtainPairSerializer):
    """Custom serializer to add claims to the token."""

    @classmethod
    def get_token(cls, user):
        """Get the token for the user."""
        token = super().get_token(user)
        token['show_guide'] = user.show_guide
        token['username'] = user.username

        user_id = token['user_id']
        token['tier'] = cls.get_user_tier(user_id, str(token))

        return token


class JwtRefreshSerializer(BaseJwtSerializer, TokenRefreshSerializer):
    """Custom serializer to add claims to the token."""

    def validate(self, attrs):
        """Validate and return a new token."""
        response = super().validate(attrs)

        refresh = RefreshToken(response['refresh'])
        refresh['tier'] = self.get_user_tier(refresh['user_id'], str(refresh))

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
