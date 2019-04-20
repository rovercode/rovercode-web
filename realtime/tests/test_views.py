"""Realtime test views."""
from test_plus.test import TestCase

from django.urls import reverse


class TestRealtimeViews(TestCase):
    """Tests the home view."""

    def test_debug_index_view(self):
        """Test the debug index view."""
        response = self.get(reverse('realtime:debug-index'))
        self.assertEqual(200, response.status_code)

    def test_debug_room_view(self):
        """Test the debug room view."""
        response = self.get(reverse('realtime:debug-room',
                                    kwargs={'room_name': 'foobar'}))
        self.assertEqual(200, response.status_code)
