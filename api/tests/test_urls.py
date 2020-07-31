"""API test urls."""
from django.urls import reverse, resolve

from test_plus.test import TestCase


class TestApiURLs(TestCase):
    """Tests the urls."""

    def test_block_diagrams_reverse(self):
        """api:v1:blockdiagram-list reverses to /api/v1/block-diagrams/."""
        self.assertEqual(
            reverse('api:v1:blockdiagram-list'),
            '/api/v1/block-diagrams/')

    def test_block_diagrams_resolve(self):
        """/api/v1/block-diagrams/ resolves to api:v1:blockdiagram-list."""
        self.assertEqual(
            resolve('/api/v1/block-diagrams/').view_name,
            'api:v1:blockdiagram-list')
