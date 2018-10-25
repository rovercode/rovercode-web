"""Channels JWT Middleware test models."""
from django.contrib.auth.models import AnonymousUser
from test_plus.test import TestCase

from unittest.mock import MagicMock, patch

from middleware.channels_jwt_middleware import ChannelsJwtMiddleware

class TestChannelsJwtMiddleware(TestCase):
    """Test Channels JWT middleware functions."""

    def test__init__(self):
        """Test the inner initialization."""
        uut = ChannelsJwtMiddleware("foobar")
        self.assertEqual("foobar", uut.inner)

    def test__call__(self):
        """Test the __call__ method."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": "foobar"}}
        with patch('rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": "some_user"}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual("some_user", scope["user"])

    def test__call__not_auth(self):
        """Test the __call__ method."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": "foobar"}}
        with patch('rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual(AnonymousUser, scope["user"])

    def test__call__no_cookie(self):
        """Test the __call__ method."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": None}}
        with patch('rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual(AnonymousUser, scope["user"])

    def test__call__no_cookies(self):
        """Test the __call__ method."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {}
        with patch('rest_framework_jwt.serializers.VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual(AnonymousUser, scope["user"])
