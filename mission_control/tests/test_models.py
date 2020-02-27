"""Mission Control test models."""
from unittest.mock import patch

from test_plus.test import TestCase

from mission_control.models import Rover, BlockDiagram


class TestRover(TestCase):
    """Tests the Rover model."""

    def test__str__(self):
        """Test the stringify method."""
        user = self.make_user()
        rover = Rover.objects.create(
            name='rover',
            owner=user
        )
        self.assertEqual(str(rover), 'rover')


class TestBlockDiagram(TestCase):
    """Tests the block diagram model."""

    def setUp(self):
        """Initialize the tests."""
        super().setUp()
        self.patcher = patch('requests.post')
        self.mock_post = self.patcher.start()
        self.mock_post.return_value.status_code = 404

        self.user = self.make_user()
        self.bd = BlockDiagram.objects.create(
            user=self.user,
            name='test',
            content='<xml></xml>'
        )

    def tearDown(self):
        """Tear down the tests."""
        super().tearDown()
        self.patcher.stop()

    def test__str__(self):
        """Test the stringify method."""
        self.assertEqual(str(self.bd), 'test')

    def test_bd(self):
        """Test the model."""
        self.assertEqual(1, BlockDiagram.objects.count())
        self.assertEqual(self.user.id, BlockDiagram.objects.first().user.id)
