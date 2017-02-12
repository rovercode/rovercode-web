from test_plus.test import TestCase

from mission_control.models import Rover, BlockDiagram


class TestRover(TestCase):

    def test__str__(self):
        self.rover = Rover.objects.create(
            name='rover',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        self.assertEqual(str(self.rover), 'rover')


class TestBlockDiagram(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.bd = BlockDiagram.objects.create(
            user=self.user,
            name='test',
            content='<xml></xml>'
        )

    def test__str__(self):
        self.assertEqual(str(self.bd), 'test')

    def test_bd(self):
        self.assertEqual(1, BlockDiagram.objects.count())
        self.assertEqual(self.user.id, BlockDiagram.objects.first().user.id)
