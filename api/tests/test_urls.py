"""API test urls."""
from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestApiURLs(TestCase):
    """Tests the urls."""

    def test_rovers_reverse(self):
        """api:v1:rover-list should reverse to /api/v1/rovers/."""
        self.assertEqual(
            reverse('api:v1:rover-list'),
            '/api/v1/rovers/')

    def test_rovers_resolve(self):
        """/api/v1/rovers/ should resolve to api:v1:rover-list."""
        self.assertEqual(
            resolve('/api/v1/rovers/').view_name,
            'api:v1:rover-list')

    def test_block_diagrams_reverse(self):
        """api:v1:blockdiagram-list should reverse to /api/v1/block-diagrams/."""
        self.assertEqual(
            reverse('api:v1:blockdiagram-list'),
            '/api/v1/block-diagrams/')

    def test_block_diagrams_resolve(self):
        """/api/v1/block-diagrams/ should resolve to api:v1:blockdiagram-list."""
        self.assertEqual(
            resolve('/api/v1/block-diagrams/').view_name,
            'api:v1:blockdiagram-list')
