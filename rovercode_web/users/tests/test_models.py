"""Models tests."""
from django.conf import settings
from django.db.models.signals import post_save
from test_plus.test import TestCase


class TestUser(TestCase):
    """Test User model."""

    def setUp(self):
        """Initialize the tests."""
        post_save.disconnect(
            sender=settings.AUTH_USER_MODEL, dispatch_uid='new_user')
        self.user = self.make_user()

    def test__str__(self):
        """Test the string representation."""
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )
