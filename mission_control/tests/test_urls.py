"""Mission Control test urls."""
from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestMissionControlURLs(TestCase):
    """Tests the urls."""

    def test_home_reverse(self):
        """mission-control:home should reverse to /mission-control/."""
        self.assertEqual(reverse('mission-control:home'), '/mission-control/')

    def test_home_resolve(self):
        """/mission-control/ should resolve to mission-control:home."""
        self.assertEqual(
            resolve('/mission-control/').view_name,
            'mission-control:home')

    def test_home_load_reverse(self):
        """mission-control:home should reverse to /mission-control/load/1."""
        self.assertEqual(
            reverse('mission-control:home_with_load', kwargs={'bd': 1}),
            '/mission-control/load/1/')

    def test_home_load_resolve(self):
        """/mission-control/load/1 should resolve to mission-control:home."""
        match = resolve('/mission-control/load/1/')
        self.assertEqual(match.view_name, 'mission-control:home_with_load')
        self.assertEqual(match.kwargs['bd'], '1')

    def test_bd_list_reverse(self):
        """mission-control:bd_list should reverse to /mission-control/bd-list/.""" # noqa
        self.assertEqual(
            reverse('mission-control:bd_list'),
            '/mission-control/bd-list/')

    def test_bd_list_resolve(self):
        """/mission-control/bd-list/ should resolve to mission-control:bd_list.""" # noqa
        self.assertEqual(
            resolve('/mission-control/bd-list/').view_name,
            'mission-control:bd_list')
