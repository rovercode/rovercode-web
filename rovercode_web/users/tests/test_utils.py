"""Utils tests."""
from django.conf import settings
from django.db.models.signals import post_save
from django.test import override_settings
from test_plus.test import TestCase

import responses
from rest_framework_simplejwt.tokens import RefreshToken

from rovercode_web.users.utils import JwtObtainPairSerializer
from rovercode_web.users.utils import JwtRefreshSerializer


@override_settings(SUBSCRIPTION_SERVICE_HOST='http://test.test')
class TestUtils(TestCase):
    """Test utils methods."""

    def setUp(self):
        """Initialize the tests."""
        post_save.disconnect(
            sender=settings.AUTH_USER_MODEL, dispatch_uid='new_user')
        self.user = self.make_user()

    @responses.activate
    def test_jwt_payload_error(self):
        """Test creating the JWT payload with external service error."""
        responses.add(
            responses.GET,
            f'http://test.test/api/v1/customer/{self.user.id}/',
            status=503
        )
        payload = JwtObtainPairSerializer.get_token(self.user)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(payload['tier'], 1)

    @responses.activate
    def test_jwt_payload(self):
        """Test creating the JWT payload."""
        responses.add(
            responses.GET,
            f'http://test.test/api/v1/customer/{self.user.id}/',
            json={'subscription': {'plan': '2'}},
            status=200
        )
        payload = JwtObtainPairSerializer.get_token(self.user)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(payload['show_guide'], self.user.show_guide)
        self.assertEqual(payload['tier'], 2)

    @responses.activate
    def test_jwt_refresh_payload(self):
        """Test refreshing the JWT payload."""
        responses.add(
            responses.GET,
            f'http://test.test/api/v1/customer/{self.user.id}/',
            json={'subscription': {'plan': '2'}},
            status=200
        )
        refresh_token = RefreshToken.for_user(self.user)
        refresh_token['show_guide'] = self.user.show_guide
        serializer = JwtRefreshSerializer(data={
            'refresh': str(refresh_token),
        })
        self.assertTrue(serializer.is_valid())
        self.assertEqual(len(responses.calls), 1)
        token = RefreshToken(serializer.validated_data['refresh'])
        self.assertEqual(token['show_guide'], self.user.show_guide)
        self.assertEqual(token['tier'], 2)
