from test_plus.test import TestCase

from django.core.urlresolvers import reverse

from mission_control.models import Rover, BlockDiagram


class TestRoverViewSet(TestCase):

    def test_rover(self):
        Rover.objects.create(
            name='rover',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        response = self.get(reverse('mission-control:rover-list'))
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['name'], 'rover')
        self.assertEqual(response.json()[0]['owner'], 'jimbo')
        self.assertEqual(response.json()[0]['local_ip'], '8.8.8.8')


class TestBlockDiagramViewSet(TestCase):

    def test_bd(self):
        user = self.make_user()
        bd = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        response = self.get(reverse('mission-control:blockdiagram-list'))
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['id'], bd.id)
        self.assertEqual(response.json()[0]['user'], user.id)
        self.assertEqual(response.json()[0]['name'], 'test')
        self.assertEqual(response.json()[0]['content'], '<xml></xml>')
