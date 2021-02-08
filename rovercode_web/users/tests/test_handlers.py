"""Handlers tests."""
from django.conf import settings
from django.db.models.signals import post_save
from django.test import override_settings
from test_plus.test import TestCase

import responses

import rovercode_web


@override_settings(SUBSCRIPTION_SERVICE_HOST='http://test.test')
class TestHandlers(TestCase):
    """Test signal handlers."""

    def setUp(self):
        """Initialize the tests."""
        post_save.connect(
            rovercode_web.users.signals.handlers.create_new_user,
            sender=settings.AUTH_USER_MODEL,
            dispatch_uid='new_user'
        )

    @responses.activate
    def test_user_create_error(self):
        """Test external user create failure."""
        responses.add(
            responses.POST,
            'http://test.test/api/v1/customer/',
            status=503
        )
        self.make_user()
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_external_user_create(self):
        """Test external user created on new user."""
        responses.add(
            responses.POST,
            'http://test.test/api/v1/customer/',
            status=200
        )
        user = self.make_user()
        self.assertEqual(len(responses.calls), 2)

        # Updating a user should do nothing
        user.email = 'test@example.com'
        user.save()
        self.assertEqual(len(responses.calls), 2)
