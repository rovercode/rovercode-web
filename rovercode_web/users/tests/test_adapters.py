"""Adapters tests."""
from test_plus.test import TestCase

from django.test.client import RequestFactory

from ..adapters import AccountAdapter, SocialAccountAdapter


class TestAdapters(TestCase):
    """Tests the adapters."""

    def setUp(self):
        """Initialize the tests."""
        self.factory = RequestFactory()

    def test_account_adapter(self):
        """Tests the account adapter."""
        request = self.factory.get('')
        result = AccountAdapter().is_open_for_signup(request)
        self.assertTrue(result)

    def test_social_account_adapter(self):
        """Tests the social account adapter."""
        request = self.factory.get('')
        # TODO: Find documentation on the sociallogin paramter.
        result = SocialAccountAdapter().is_open_for_signup(request, None)
        self.assertTrue(result)
