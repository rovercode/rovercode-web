"""Mission Control test views."""
from test_plus.test import TestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from mission_control.models import BlockDiagram


class TestHomeView(TestCase):
    """Tests the home view."""

    def test_home(self):
        """Test the home view."""
        response = self.get(reverse('mission-control:home'))
        self.assertEqual(200, response.status_code)


class BaseAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Initialize the tests."""
        self.admin = get_user_model().objects.create_user(
            username='administrator',
            email='admin@example.com',
            password='password'
        )


class TestHomeViewWithLoad(BaseAuthenticatedTestCase):
    """Tests the home view loading a block diagram."""

    def test_home_load(self):
        """Test the home view loading a block diagram."""
        self.client.login(username='administrator', password='password')
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )
        response = self.get(reverse(
            'mission-control:home_with_load', kwargs={'bd': bd.id}))
        self.assertEqual(200, response.status_code)

    def test_home_load_nonexistant(self):
        """Test the home view tring to load a nonexistant block diagram."""
        self.client.login(username='administrator', password='password')
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )
        response = self.get(reverse(
            'mission-control:home_with_load', kwargs={'bd': bd.id + 1}))
        self.assertEqual(404, response.status_code)


class TestBlockDiagramListView(BaseAuthenticatedTestCase):
    """Tests the block diagram list view."""

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
        response = self.get(reverse('mission-control:bd_list'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.admin.username)
        self.assertContains(response, bd2.name)
        self.assertNotContains(response, bd1.name)

    def test_list_not_logged_in(self):
        """Test the block diagram list view redirects if no logged in user."""
        response = self.get(reverse('mission-control:bd_list'))
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' +
            reverse('mission-control:bd_list'))
