"""Mission Control test views."""
from test_plus.test import TestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from mission_control.models import Rover, BlockDiagram

import time


class TestHomeView(TestCase):
    """Tests the home view."""

    def test_home(self):
        """Test the home view."""
        response = self.get(reverse('mission-control:home'))
        self.assertEqual(200, response.status_code)


class TestListView(TestCase):
    """Tests the block diagram list view."""

    def setUp(self):
        """Setup the tests."""
        self.admin = get_user_model().objects.create(username='administrator')
        self.admin.set_password('password')
        self.admin.save()

    def test_list(self):
        """Test the block diagram list view displays the correct items."""
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
        """Test the block diagram list view redirects if no logged in user."""
        response = self.get(reverse('mission-control:list'))
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' +
            reverse('mission-control:list'))


class TestRoverViewSet(TestCase):
    """Tests the rover API view."""

    def test_rover(self):
        """Test the rover view displays the correct items."""
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
    """Tests the block diagram API view."""

    def test_bd(self):
        """Test the block diagram API view displays the correct items."""
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
        """Test the block diagram API view filters on user correctly."""
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
