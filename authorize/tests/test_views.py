"""Authorize test views."""
import re
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from django.urls import reverse
from test_plus.test import TestCase
import responses

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialLogin
from rest_auth.registration.serializers import SocialLoginSerializer

from ..views import GitHubCallbackConnect
from ..views import GitHubCallbackCreate
from ..views import GoogleCallbackConnect
from ..views import GoogleCallbackCreate


class AuthorizationUrlTestCase(TestCase):
    """Test the authorization urls."""

    def test_github_authorization_url(self):
        """Test the Github authorization url."""
        social_app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='1234',
            secret='5678'
        )
        social_app.sites.add(Site.objects.first())
        social_app.save()

        response = self.client.post(reverse('jwt:github_auth_server'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())
        self.assertIn('github', response.json()['url'])

    def test_google_authorization_url(self):
        """Test the Google authorization url."""
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='1234',
            secret='5678'
        )
        social_app.sites.add(Site.objects.first())
        social_app.save()

        response = self.client.post(reverse('jwt:google_auth_server'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())
        self.assertIn('google', response.json()['url'])


class CallbackUrlTestCase(TestCase):
    """Test the callback urls."""

    def setUp(self):
        """Initialize the tests."""
        self.admin = get_user_model().objects.create_user(
            username='administrator',
            email='admin@example.com',
            password='password'
        )

    def test_github_callback_url(self):
        """Test the Github callback url."""
        create = GitHubCallbackCreate()

        with self.settings(SOCIAL_CALLBACK_URL='http://test.com/{service}/'):
            self.assertEqual(create.callback_url, 'http://test.com/github/')

    def test_google_callback_url(self):
        """Test the Google callback url."""
        create = GoogleCallbackCreate()

        with self.settings(SOCIAL_CALLBACK_URL='http://test.com/{service}/'):
            self.assertEqual(create.callback_url, 'http://test.com/google/')

    def test_github_connection_response(self):
        """Test the Github connection response."""
        connect = GitHubCallbackConnect()

        self.assertEqual(connect.get_response().status_code, 200)

    def test_google_connection_response(self):
        """Test the Google connection response."""
        connect = GoogleCallbackConnect()

        self.assertEqual(connect.get_response().status_code, 200)

    @responses.activate
    @patch.object(SocialLoginSerializer, 'validate')
    @patch.object(SocialLogin, 'verify_and_unstash_state')
    @override_settings(SUBSCRIPTION_SERVICE_HOST='http://test.test')
    def test_github_login(self, mock_verify, mock_validate):
        """Test the Github login returns a JWT."""
        responses.add(
            responses.GET,
            re.compile(r'http://test.test/api/v1/customer/\d+/'),
            json={'subscription': {'plan': '2'}},
            status=200
        )
        mock_validate.return_value = {
            'user': self.admin,
        }
        mock_verify.return_value = None

        social_app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='1234',
            secret='5678'
        )
        social_app.sites.add(Site.objects.first())
        social_app.save()

        response = self.client.post(reverse('jwt:github_callback_login'), {
            'state': '1234',
            'code': '5678'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(responses.calls), 1)
        self.assertIn('token', response.json())

    @responses.activate
    @patch.object(SocialLoginSerializer, 'validate')
    @patch.object(SocialLogin, 'verify_and_unstash_state')
    @override_settings(SUBSCRIPTION_SERVICE_HOST='http://test.test')
    def test_google_login(self, mock_verify, mock_validate):
        """Test the Google login returns a JWT."""
        responses.add(
            responses.GET,
            re.compile(r'http://test.test/api/v1/customer/\d+/'),
            json={'subscription': {'plan': '2'}},
            status=200
        )
        mock_validate.return_value = {
            'user': self.admin,
        }
        mock_verify.return_value = None

        social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='1234',
            secret='5678'
        )
        social_app.sites.add(Site.objects.first())
        social_app.save()

        response = self.client.post(reverse('jwt:google_callback_login'), {
            'state': '1234',
            'code': '5678'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(responses.calls), 1)
        self.assertIn('token', response.json())

    @patch.object(SocialLogin, 'verify_and_unstash_state')
    def test_state_validation(self, mock_verify):
        """Test the state validation."""
        mock_verify.side_effect = PermissionDenied()

        response = self.client.post(reverse('jwt:google_callback_login'), {
            'state': '1234',
            'code': '5678'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('state', response.json())
        self.assertEqual('State did not match.', response.json()['state'][0])
