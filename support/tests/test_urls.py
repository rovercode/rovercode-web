"""Support test urls."""
from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestSupportURLs(TestCase):
    """Tests the urls."""

    def test_index_reverse(self):
        """support:debug-index should reverse to /support/."""
        self.assertEqual(reverse('support:debug-index'), '/support/')

    def test_home_resolve(self):
        """/support/ should resolve to support:debug-index."""
        self.assertEqual(
            resolve('/support/').view_name,
            'support:debug-index')

    def test_room_reverse(self):
        """support:room-index named foo should reverse to /support/foo."""
        self.assertEqual(reverse('support:debug-room',
                                 kwargs={'room_name': 'foo'}),
                         '/support/foo/')

    def test_room_resolve(self):
        """/support/foobar should resolve to support:debug-room."""
        self.assertEqual(
            resolve('/support/foobar/').view_name,
            'support:debug-room')
