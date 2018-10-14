"""Support test views."""
from test_plus.test import TestCase

from django.core.urlresolvers import reverse


class TestSupportViews(TestCase):
    """Tests the home view."""

    def test_debug_index_view(self):
        """Test the debug index view."""
        response = self.get(reverse('support:debug-index'))
        self.assertEqual(200, response.status_code)

    def test_debug_room_view(self):
        """Test the debug room view."""
        response = self.get(reverse('support:debug-room',
                                    kwargs={'room_name': 'foobar'}))
        self.assertEqual(200, response.status_code)
