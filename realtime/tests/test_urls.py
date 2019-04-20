"""Realtime test urls."""
from django.urls import reverse, resolve

from test_plus.test import TestCase


class TestRealtimeURLs(TestCase):
    """Tests the urls."""

    def test_index_reverse(self):
        """realtime:debug-index should reverse to /realtime/."""
        self.assertEqual(reverse('realtime:debug-index'), '/realtime/')

    def test_home_resolve(self):
        """/realtime/ should resolve to realtime:debug-index."""
        self.assertEqual(
            resolve('/realtime/').view_name,
            'realtime:debug-index')

    def test_room_reverse(self):
        """realtime:room-index named foo should reverse to /realtime/foo."""
        self.assertEqual(reverse('realtime:debug-room',
                                 kwargs={'room_name': 'foo'}),
                         '/realtime/foo/')

    def test_room_resolve(self):
        """/realtime/foobar should resolve to realtime:debug-room."""
        self.assertEqual(
            resolve('/realtime/foobar/').view_name,
            'realtime:debug-room')
