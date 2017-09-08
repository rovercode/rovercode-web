"""API test apps."""
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from test_plus.test import TestCase

from mission_control.models import Rover
from oauth2_provider.models import Application


class TestApiApps(TestCase):
    """Tests the apps."""

    def test_access_token(self):
        """Test access token can access API."""
        admin = get_user_model().objects.create_user(
            username='administrator',
            email='admin@example.com',
            password='password'
        )

        app = Application.objects.create(
            user=admin,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_type=Application.CLIENT_CONFIDENTIAL,
            name='Sparky'
        )

        token_info = {
            'grant_type': 'client_credentials',
            'client_id': app.client_id,
            'client_secret': app.client_secret,
        }

        response = self.client.post(
            reverse('oauth2_provider:token'), token_info)

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

        access_token = response.json()['access_token']

        Rover.objects.create(
            name='rover',
            owner=admin,
            local_ip='8.8.8.8'
        )
        Rover.objects.create(
            name='rover2',
            owner=self.make_user(),
            local_ip='8.8.8.8'
        )

        response = self.client.get(
            reverse('api:v1:rover-list'),
            HTTP_AUTHORIZATION='Bearer {0}'.format(access_token))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['name'], 'rover')
        self.assertEqual(response.json()[0]['owner'], admin.id)
        self.assertEqual(response.json()[0]['local_ip'], '8.8.8.8')
