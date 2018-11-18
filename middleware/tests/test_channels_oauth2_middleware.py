"""Channels OAuth2 Middleware test models."""
from unittest.mock import MagicMock, patch
from django.contrib.auth.models import AnonymousUser
from test_plus.test import TestCase


from middleware.channels_oauth2_middleware import ChannelsOAuth2Middleware


class TestChannelsOauth2Middleware(TestCase):
    """Test Channels OAuth2 middleware functions."""

    def test__init__(self):
        """Test the inner initialization."""
        uut = ChannelsOAuth2Middleware("foobar")
        self.assertEqual("foobar", uut.inner)

    def test__call__(self):
        """Test the __call__ method."""
        inner = MagicMock()
        uut = ChannelsOAuth2Middleware(inner)
        scope = {"headers": [(b'authorization', b'baz')], "path": "/asdf"}
        with patch('middleware.channels_oauth2_middleware.get_oauthlib_core') \
                as get_oauthlib_core:
            oauthlib_core = MagicMock()
            mock_oauth_response = MagicMock()
            mock_oauth_response.user = 'test_user'
            oauthlib_core.verify_request.return_value = \
                (True, mock_oauth_response)
            get_oauthlib_core.return_value = oauthlib_core

            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual("test_user", scope["user"])

    def test__call__not_auth(self):
        """Test the __call__ method when the token is not for a valid user."""
        inner = MagicMock()
        uut = ChannelsOAuth2Middleware(inner)
        scope = {"headers": [(b'authorization', b'baz')], "path": "/asdf"}
        with patch('middleware.channels_oauth2_middleware.get_oauthlib_core') \
                as get_oauthlib_core:
            oauthlib_core = MagicMock()
            mock_oauth_response = MagicMock()
            mock_oauth_response.user = 'test_user'
            oauthlib_core.verify_request.return_value = (False, None)
            get_oauthlib_core.return_value = oauthlib_core

            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual(AnonymousUser, scope["user"])

    def test__call__no_token(self):
        """Test the __call__ method when there is no token."""
        inner = MagicMock()
        uut = ChannelsOAuth2Middleware(inner)
        scope = {"path": "/asdf"}
        uut.__call__(scope)
        inner.assert_called_once_with(scope)
        self.assertEqual(AnonymousUser, scope["user"])
