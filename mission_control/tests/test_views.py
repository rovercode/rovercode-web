"""Mission Control test views."""
from test_plus.test import TestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from mission_control.models import Rover, BlockDiagram


class TestHomeView(TestCase):
    """Tests the home view."""

    def test_home(self):
        """Test the home view."""
        response = self.get(reverse('mission-control:home'))
        self.assertEqual(200, response.status_code)


class BaseAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Setup the tests."""
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


class TestRoverListView(BaseAuthenticatedTestCase):
    """Tests the rover list view."""

    def test_list(self):
        """Test the rover list view displays the correct items."""
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        rover1 = Rover.objects.create(
            name='rover1',
            owner=user,
            local_ip='192.168.1.100'
        )
        rover2 = Rover.objects.create(
            name='rover2',
            owner=self.admin,
            local_ip='192.168.1.200'
        )
        response = self.get(reverse('mission-control:rover_list'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.admin.username)
        self.assertContains(response, rover2.name)
        self.assertNotContains(response, rover1.name)

    def test_list_not_logged_in(self):
        """Test the rover list view redirects if no logged in user."""
        response = self.get(reverse('mission-control:rover_list'))
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' +
            reverse('mission-control:rover_list'))


class TestRoverSettingsView(BaseAuthenticatedTestCase):
    """Tests the rover settings view."""

    def test_new_rover_form(self):
        """Test getting a form for a new rover."""
        self.client.login(username='administrator', password='password')
        response = self.get(reverse('mission-control:rover_new'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'New Rover')

    def test_new_rover_save(self):
        """Test creating a new rover."""
        self.client.login(username='administrator', password='password')
        settings = {
            'name': 'rover123',
            'left_forward_pin': 'a',
            'left_backward_pin': 'b',
            'right_forward_pin': 'c',
            'right_backward_pin': 'd',
            'left_eye_pin': 'e',
            'right_eye_pin': 'f',
            'left_eye_i2c_port': 0,
            'left_eye_i2c_addr': 1,
            'right_eye_i2c_port': 2,
            'right_eye_i2c_addr': 3,
            'local_ip': '192.169.1.200',
        }
        response = self.client.post(
            reverse('mission-control:rover_new'),
            settings)
        self.assertEqual(200, response.status_code)
        rover_obj = Rover.objects.get(name='rover123')
        self.assertEqual(rover_obj.owner, self.admin)
        self.assertEqual(rover_obj.name, settings['name'])
        self.assertEqual(
            rover_obj.left_forward_pin, settings['left_forward_pin'])
        self.assertEqual(
            rover_obj.right_forward_pin, settings['right_forward_pin'])
        self.assertEqual(
            rover_obj.left_backward_pin, settings['left_backward_pin'])
        self.assertEqual(
            rover_obj.right_backward_pin, settings['right_backward_pin'])
        self.assertEqual(
            rover_obj.left_eye_pin, settings['left_eye_pin'])
        self.assertEqual(
            rover_obj.right_eye_pin, settings['right_eye_pin'])
        self.assertEqual(
            rover_obj.right_eye_i2c_port, settings['right_eye_i2c_port'])
        self.assertEqual(
            rover_obj.right_eye_i2c_addr, settings['right_eye_i2c_addr'])
        self.assertEqual(
            rover_obj.left_eye_i2c_port, settings['left_eye_i2c_port'])
        self.assertEqual(
            rover_obj.left_eye_i2c_addr, settings['left_eye_i2c_addr'])
        self.assertEqual(
            rover_obj.oauth_application.user, self.admin
        )
        self.assertTrue(
            rover_obj.oauth_application.client_id
        )
        self.assertTrue(
            rover_obj.oauth_application.client_secret
        )

    def test_display_settings(self):
        """Test the rover settings view displays the correct items."""
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        Rover.objects.create(
            name='rover1',
            owner=user,
            local_ip='192.168.1.100'
        )
        rover2 = Rover.objects.create(
            name='rover2',
            owner=self.admin,
            local_ip='192.168.1.200'
        )
        response = self.get(
            reverse('mission-control:rover_settings',
                    kwargs={'pk': rover2.pk})
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, rover2.name)

    def test_display_settings_not_own_rover(self):
        """Test the rover settings view when not user's rover."""
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        rover1 = Rover.objects.create(
            name='rover1',
            owner=user,
            local_ip='192.168.1.100'
        )
        Rover.objects.create(
            name='rover2',
            owner=self.admin,
            local_ip='192.168.1.200'
        )
        response = self.get(
            reverse('mission-control:rover_settings',
                    kwargs={'pk': rover1.pk})
        )
        self.assertEqual(404, response.status_code)

    def test_change_settings(self):
        """Test changing the rover settings."""
        self.client.login(username='administrator', password='password')
        rover = Rover.objects.create(
            name='rover1',
            owner=self.admin,
            local_ip='192.168.1.100'
        )
        settings = {
            'name': 'rover1',
            'left_forward_pin': 'a',
            'left_backward_pin': 'b',
            'right_forward_pin': 'c',
            'right_backward_pin': 'd',
            'left_eye_pin': 'e',
            'right_eye_pin': 'f',
            'left_eye_i2c_port': 0,
            'left_eye_i2c_addr': 1,
            'right_eye_i2c_port': 2,
            'right_eye_i2c_addr': 3
        }
        response = self.client.post(
            reverse('mission-control:rover_settings', kwargs={'pk': rover.pk}),
            settings)
        self.assertEqual(200, response.status_code)
        rover_obj = Rover.objects.get(pk=rover.pk)
        self.assertEqual(rover_obj.name, settings['name'])
        self.assertEqual(
            rover_obj.left_forward_pin, settings['left_forward_pin'])
        self.assertEqual(
            rover_obj.right_forward_pin, settings['right_forward_pin'])
        self.assertEqual(
            rover_obj.left_backward_pin, settings['left_backward_pin'])
        self.assertEqual(
            rover_obj.right_backward_pin, settings['right_backward_pin'])
        self.assertEqual(
            rover_obj.left_eye_pin, settings['left_eye_pin'])
        self.assertEqual(
            rover_obj.right_eye_pin, settings['right_eye_pin'])
        self.assertEqual(
            rover_obj.right_eye_i2c_port, settings['right_eye_i2c_port'])
        self.assertEqual(
            rover_obj.right_eye_i2c_addr, settings['right_eye_i2c_addr'])
        self.assertEqual(
            rover_obj.left_eye_i2c_port, settings['left_eye_i2c_port'])
        self.assertEqual(
            rover_obj.left_eye_i2c_addr, settings['left_eye_i2c_addr'])
        self.assertEqual(
            rover_obj.oauth_application.user, self.admin
        )
        self.assertTrue(
            rover_obj.oauth_application.client_id
        )
        self.assertTrue(
            rover_obj.oauth_application.client_secret
        )

    def test_change_settings_invalid(self):
        """Test changing the rover settings with invalid settings."""
        self.client.login(username='administrator', password='password')
        rover = Rover.objects.create(
            name='rover1',
            owner=self.admin,
            local_ip='192.168.1.100'
        )
        settings = {}
        response = self.client.post(
            reverse('mission-control:rover_settings', kwargs={'pk': rover.pk}),
            settings)
        self.assertEqual(200, response.status_code)

    def test_rover_settings_not_logged_in(self):
        """Test the rover settings view redirects if no logged in user."""
        response = self.get(
            reverse('mission-control:rover_settings', kwargs={'pk': '1'}))
        self.assertRedirects(
            response,
            reverse('account_login') + '?next=' +
            reverse('mission-control:rover_settings', kwargs={'pk': '1'}))
