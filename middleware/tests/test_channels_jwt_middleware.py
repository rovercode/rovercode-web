"""Channels JWT Middleware test models."""
from unittest.mock import MagicMock, patch
from test_plus.test import TestCase
from rest_framework.exceptions import ValidationError


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
        with patch('rest_framework_jwt.serializers.'
                   'VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": "some_user"}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertEqual("some_user", scope["user"])

    def test__call__already_auth(self):
        """Test the __call__ method if there is already an user."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        user = self.make_user()
        scope = {"cookies": {"auth_jwt": "foobar"}, "user": user}
        uut.__call__(scope)
        inner.assert_called_once_with(scope)
        self.assertEqual(user, scope["user"])

    def test__call__not_auth(self):
        """Test the __call__ method if the user is not authorized."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": "foobar"}}
        with patch('rest_framework_jwt.serializers.'
                   'VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertFalse("user" in scope)

    def test__call__validation_error(self):
        """Test the __call__ method when a jwt that does not authorize."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": "foobar"}}
        with patch('rest_framework_jwt.serializers.'
                   'VerifyJSONWebTokenSerializer.validate') as validate:
            validate.side_effect = ValidationError()
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertFalse("user" in scope)

    def test__call__no_cookie(self):
        """Test the __call__ method if the needed cookie is absent."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {"cookies": {"auth_jwt": None}}
        with patch('rest_framework_jwt.serializers.'
                   'VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertFalse("user" in scope)

    def test__call__no_cookies(self):
        """Test the __call__ method if there are no cookies at all."""
        inner = MagicMock()
        uut = ChannelsJwtMiddleware(inner)
        scope = {}

        with patch('rest_framework_jwt.serializers.'
                   'VerifyJSONWebTokenSerializer.validate') as validate:
            validate.return_value = {"user": None}
            uut.__call__(scope)
            inner.assert_called_once_with(scope)
            self.assertFalse("user" in scope)
