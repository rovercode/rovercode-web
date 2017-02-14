from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestMissionControlURLs(TestCase):

    def test_home_reverse(self):
        """mission-control-home should reverse to /mission-control/."""
        self.assertEqual(reverse('mission-control-home'), '/mission-control/')

    def test_home_resolve(self):
        """/mission-control/ should resolve to mission-control-home."""
        self.assertEqual(
            resolve('/mission-control/').view_name,
            'mission-control-home')

    def test_rovers_reverse(self):
        """rover-list should reverse to /mission-control/rovers/."""
        self.assertEqual(reverse('rover-list'), '/mission-control/rovers/')

    def test_rovers_resolve(self):
        """/mission-control/rovers/ should resolve to rover-list."""
        self.assertEqual(
            resolve('/mission-control/rovers/').view_name,
            'rover-list')

    def test_block_diagrams_reverse(self):
        """blockdiagram-list should reverse to /mission-control/block-diagrams/."""
        self.assertEqual(
            reverse('blockdiagram-list'),
            '/mission-control/block-diagrams/')

    def test_block_diagrams_resolve(self):
        """/mission-control/block-diagrams/ should resolve to blockdiagram-list."""
        self.assertEqual(
            resolve('/mission-control/block-diagrams/').view_name,
            'blockdiagram-list')
