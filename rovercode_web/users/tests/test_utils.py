"""Utils tests."""
from django.test import override_settings
from test_plus.test import TestCase

import responses

from rovercode_web.users.utils import jwt_payload_handler


@override_settings(SUBSCRIPTION_SERVICE_HOST='http://test.test')
class TestUtils(TestCase):
    """Test utils methods."""

    def setUp(self):
        """Initialize the tests."""
        self.user = self.make_user()

    @responses.activate
    def test_jwt_payload_error(self):
        """Test creating the JWT payload with external service error."""
        responses.add(
            responses.GET,
            f'http://test.test/api/v1/customer/{self.user.id}/',
            status=503
        )
        payload = jwt_payload_handler(self.user)
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
        payload = jwt_payload_handler(self.user)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(payload['show_guide'], self.user.show_guide)
        self.assertEqual(payload['tier'], 2)
