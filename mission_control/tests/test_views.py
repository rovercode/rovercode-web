from test_plus.test import TestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from mission_control.models import Rover, BlockDiagram

import time


class TestListView(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create(username='administrator')
        self.admin.set_password('password')
        self.admin.save()

    def test_list(self):
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        bd1 = BlockDiagram.objects.create(
            user=user,
            name='user_bd',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=self.admin,
            name='admin_bd',
            content='<xml></xml>'
        )
        response = self.get(reverse('mission-control:list'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.admin.username)
        self.assertContains(response, bd2.name)
        self.assertNotContains(response, bd1.name)

    def test_list_not_logged_in(self):
        response = self.get(reverse('mission-control:list'))
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' +
            reverse('mission-control:list'))


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
        time.sleep(6)
        Rover.objects.create(
            name='rover2',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        response = self.get(reverse('mission-control:rover-list'))
        self.assertEqual(1, len(response.json()))


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

    def test_bd_user_filter(self):
        user1 = self.make_user('user1')
        user2 = self.make_user('user2')
        BlockDiagram.objects.create(
            user=user1,
            name='test1',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=user2,
            name='test2',
            content='<xml></xml>'
        )
        response = self.get(
            reverse(
                'mission-control:blockdiagram-list') + '?user=' + str(user2.id))
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['id'], bd2.id)
        self.assertEqual(response.json()[0]['user'], user2.id)
        self.assertEqual(response.json()[0]['name'], 'test2')
        self.assertEqual(response.json()[0]['content'], '<xml></xml>')
