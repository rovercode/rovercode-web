"""Models tests."""
from test_plus.test import TestCase


class TestUser(TestCase):
    """Test User model."""

    def setUp(self):
        """Initialize the tests."""
        self.user = self.make_user()

    def test__str__(self):
        """Test the string representation."""
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )
