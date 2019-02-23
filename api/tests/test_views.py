"""API test views."""
from test_plus.test import TestCase

import dateutil.parser
import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from urllib.parse import urlencode

from oauth2_provider.models import Application
from mission_control.models import Rover, BlockDiagram


class BaseAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Initialize the tests."""
        self.admin = get_user_model().objects.create_user(
            username='administrator',
            email='admin@example.com',
            password='password'
        )
        self.client = APIClient()

    def authenticate(self):
        """Authenticate the test client."""
        credentials = {
            'username': 'administrator',
            'password': 'password',
        }
        response = self.client.post(
            reverse('api:api-token-auth'),
            data=json.dumps(credentials),
            content_type='application/json')

        self.assertEqual(200, response.status_code)

        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(response.json()['token']))


class TestRoverViewSet(BaseAuthenticatedTestCase):
    """Tests the rover API view."""

    def test_rover_create(self):
        """Test the rover registration interface."""
        self.authenticate()
        rover_info = {'name': 'Curiosity', 'local_ip': '192.168.0.10'}
        default_rover_config = {'some_setting': 'foobar'}
        # Create the rover
        with self.settings(DEFAULT_ROVER_CONFIG=default_rover_config):
            response = self.client.post(
                reverse('api:v1:rover-list'), rover_info)
        id = response.data['id']
        self.assertIn('client_id', response.data)
        self.assertIn('client_secret', response.data)
        creation_time = dateutil.parser.parse(response.data['last_checkin'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['config'], default_rover_config)

        application = Application.objects.get(client_id=response.data['client_id'])
        self.assertEqual(application.user.id, self.admin.id)

        # Try and fail to create the same rover again
        response = self.client.post(reverse('api:v1:rover-list'), rover_info)
        self.assertEqual(response.status_code, 400)

        # Update the rover
        response = self.client.put(
            reverse('api:v1:rover-detail', kwargs={'pk': id}),
            urlencode(rover_info),
            content_type="application/x-www-form-urlencoded"
        )
        checkin_time = dateutil.parser.parse(response.data['last_checkin'])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(checkin_time, creation_time)

    def test_rover_create_custom_config(self):
        """Test the rover registration with a custom config."""
        self.authenticate()
        config = {'some_field': True}
        rover_info = {'name': 'Curiosity', 'local_ip': '192.168.0.10',
                      'config': json.dumps(config)}
        # Create the rover
        response = self.client.post(
            reverse('api:v1:rover-list'), rover_info)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['config'], config)

    def test_rover_create_invalid_config(self):
        """Test the rover registration with invalid config."""
        self.authenticate()
        rover_info = {'name': 'Curiosity', 'local_ip': '192.168.0.10',
                      'config': 'not-valid-json'}

        # Create the rover
        response = self.client.post(
            reverse('api:v1:rover-list'), rover_info)
        self.assertEqual(response.status_code, 400)


    def test_rover(self):
        """Test the rover view displays the correct items."""
        self.authenticate()
        Rover.objects.create(
            name='rover',
            owner=self.admin,
            local_ip='8.8.8.8'
        )
        Rover.objects.create(
            name='rover2',
            owner=self.make_user(),
            local_ip='8.8.8.8'
        )
        response = self.get(reverse('api:v1:rover-list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['name'], 'rover')
        self.assertEqual(response.json()[0]['owner'], self.admin.id)
        self.assertEqual(response.json()[0]['local_ip'], '8.8.8.8')

    def test_rover_name_filter(self):
        """Test the rover view filters correctly on name."""
        self.authenticate()
        Rover.objects.create(
            name='rover',
            owner=self.admin,
            local_ip='8.8.8.8'
        )
        rover2 = Rover.objects.create(
            name='rover2',
            owner=self.admin,
            local_ip='8.8.8.8'
        )
        response = self.get(
            reverse('api:v1:rover-list') + '?name=' + rover2.name)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['name'], 'rover2')
        self.assertEqual(response.json()[0]['owner'], self.admin.id)
        self.assertEqual(response.json()[0]['local_ip'], '8.8.8.8')

    def test_rover_client_id_filter(self):
        """Test the rover view filters correctly on oauth application client id."""
        self.authenticate()
        Rover.objects.create(
            name='rover',
            owner=self.admin,
            local_ip='8.8.8.8',
            oauth_application = Application.objects.create(
                user=self.admin,
                authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
                client_type=Application.CLIENT_CONFIDENTIAL,
                name='rover'
            )
        )
        rover2 = Rover.objects.create(
            name='rover2',
            owner=self.admin,
            local_ip='8.8.8.8',
            oauth_application = Application.objects.create(
                user=self.admin,
                authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
                client_type=Application.CLIENT_CONFIDENTIAL,
                name='rover2'
            )
        )
        response = self.get(
            reverse('api:v1:rover-list') + '?client_id=' + rover2.oauth_application.client_id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['name'], 'rover2')
        self.assertEqual(response.json()[0]['owner'], self.admin.id)
        self.assertEqual(response.json()[0]['local_ip'], '8.8.8.8')

    def test_rover_not_logged_in(self):
        """Test the rover view denies unauthenticated user."""
        response = self.get(reverse('api:v1:rover-list'))
        self.assertEqual(401, response.status_code)


class TestBlockDiagramViewSet(BaseAuthenticatedTestCase):
    """Tests the block diagram API view."""

    def test_bd(self):
        """Test the block diagram API view displays the correct items."""
        self.authenticate()
        user = self.make_user()
        bd1 = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        response = self.get(reverse('api:v1:blockdiagram-list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertEqual(response.json()[0]['id'], bd1.id)
        self.assertEqual(response.json()[0]['user'], self.admin.id)
        self.assertEqual(response.json()[0]['name'], 'test')
        self.assertEqual(response.json()[0]['content'], '<xml></xml>')
        self.assertEqual(response.json()[1]['id'], bd2.id)
        self.assertEqual(response.json()[1]['user'], user.id)
        self.assertEqual(response.json()[1]['name'], 'test1')
        self.assertEqual(response.json()[1]['content'], '<xml></xml>')

    def test_bd_user_filter(self):
        """Test the block diagram API view filters on user correctly."""
        self.authenticate()
        user1 = self.make_user('user1')
        BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        bd = BlockDiagram.objects.create(
            user=user1,
            name='test2',
            content='<xml></xml>'
        )
        response = self.get(
            reverse('api:v1:blockdiagram-list') +
            '?user=' + str(user1.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['id'], bd.id)
        self.assertEqual(response.json()[0]['user'], user1.id)
        self.assertEqual(response.json()[0]['name'], 'test2')
        self.assertEqual(response.json()[0]['content'], '<xml></xml>')

    def test_bd_not_logged_in(self):
        """Test the block diagram view denies unauthenticated user."""
        response = self.get(reverse('api:v1:blockdiagram-list'))
        self.assertEqual(401, response.status_code)

    def test_bd_create(self):
        """Test creating block diagram sets user."""
        self.authenticate()
        data = {
            'name': 'test',
            'content': '<xml></xml>'
        }
        response = self.client.post(
            reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, data['name'])

    def test_bd_update_as_valid_user(self):
        """Test updating block diagram as owner."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        data = {
            'name': 'test',
        }
        response = self.client.patch(
            reverse(
                'api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test')

    def test_bd_update_as_invalid_user(self):
        """Test updating block diagram as another user."""
        self.authenticate()
        user = self.make_user()
        bd = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        data = {
            'name': 'test',
        }
        response = self.client.patch(
            reverse(
                'api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.content,
            b'["You may only modify your own block diagrams"]')
        self.assertEqual(BlockDiagram.objects.last().user.id, user.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test1')
