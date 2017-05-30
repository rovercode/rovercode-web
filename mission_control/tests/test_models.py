"""Mission Control test models."""
from test_plus.test import TestCase

from mission_control.models import Rover, BlockDiagram


class TestRover(TestCase):
    """Tests the Rover model."""

    def test__str__(self):
        """Test the stringify method."""
        user = self.make_user()
        self.rover = Rover.objects.create(
            name='rover',
            owner=user,
            local_ip='8.8.8.8'
        )
        self.assertEqual(str(self.rover), 'rover')


class TestBlockDiagram(TestCase):
    """Tests the block diagram model."""

    def setUp(self):
        """Setup the tests."""
        self.user = self.make_user()
        self.bd = BlockDiagram.objects.create(
            user=self.user,
            name='test',
            content='<xml></xml>'
        )

    def test__str__(self):
        """Test the stringify method."""
        self.assertEqual(str(self.bd), 'test')

    def test_bd(self):
        """Test the model."""
        self.assertEqual(1, BlockDiagram.objects.count())
        self.assertEqual(self.user.id, BlockDiagram.objects.first().user.id)
