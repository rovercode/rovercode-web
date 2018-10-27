"""API test views."""
from test_plus.test import TestCase

import dateutil.parser
import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from urllib.parse import urlencode

from oauth2_provider.models import Application
from mission_control.models import Rover, BlockDiagram
from support.models import SupportRequest


class BaseAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Initialize the tests."""
        self.admin = get_user_model().objects.create_user(
            username='administrator',
            email='admin@example.com',
            password='password'
        )


class TestRoverViewSet(BaseAuthenticatedTestCase):
    """Tests the rover API view."""

    def test_rover_create(self):
        """Test the rover registration interface."""
        self.client.login(username='administrator', password='password')
        rover_info = {'name': 'Curiosity', 'local_ip': '192.168.0.10'}

        # Create the rover
        response = self.client.post(
            reverse('api:v1:rover-list'), rover_info)
        id = response.data['id']
        creation_time = dateutil.parser.parse(response.data['last_checkin'])
        self.assertEqual(response.status_code, 201)

        # Try and fail to create the same rover again
        with self.assertRaises(IntegrityError):
            self.client.post(reverse('api:v1:rover-list'), rover_info)

        # Update the rover
        response = self.client.put(
            reverse('api:v1:rover-detail', kwargs={'pk': id}),
            urlencode(rover_info),
            content_type="application/x-www-form-urlencoded"
        )
        checkin_time = dateutil.parser.parse(response.data['last_checkin'])
        self.assertEqual(response.status_code, 200)
        self.assertGreater(checkin_time, creation_time)

    def test_rover(self):
        """Test the rover view displays the correct items."""
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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
        self.client.login(username='administrator', password='password')
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


class TestSupportRequestViewSet(BaseAuthenticatedTestCase):
    """Tests the support request API view."""

    def test_support_request(self):
        """Test the supportrequest API view displays the correct items."""
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=user,
            name='test2',
            content='<xml></xml>'
        )
        sr1 = SupportRequest.objects.create(
            owner=self.admin,
            subject='Help 1',
            body='Foo',
            experience_level=1,
            category='DEBUG',
            program=bd1
        )
        sr2 = SupportRequest.objects.create(
            owner=self.admin,
            subject='Help 2',
            body='Bar',
            experience_level=2,
            category='WHAT_NEXT',
            program=bd2
        )
        response = self.get(reverse('api:v1:supportrequest-list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertEqual(response.json()[0]['id'], sr1.id)
        self.assertEqual(response.json()[0]['owner'], self.admin.id)
        self.assertEqual(response.json()[0]['subject'], sr1.subject)
        self.assertEqual(response.json()[0]['body'], sr1.body)
        self.assertEqual(response.json()[0]['experience_level'], sr1.experience_level)
        self.assertEqual(response.json()[0]['category'], sr1.category)
        self.assertEqual(response.json()[0]['program'], sr1.program.id)
        self.assertEqual(response.json()[1]['id'], sr2.id)
        self.assertEqual(response.json()[1]['owner'], self.admin.id)
        self.assertEqual(response.json()[1]['subject'], sr2.subject)
        self.assertEqual(response.json()[1]['body'], sr2.body)
        self.assertEqual(response.json()[1]['experience_level'], sr2.experience_level)
        self.assertEqual(response.json()[1]['category'], sr2.category)
        self.assertEqual(response.json()[1]['program'], sr2.program.id)


    def test_support_request_owner_filter(self):
        """Test the support request API view filters on owner correctly."""
        self.client.login(username='administrator', password='password')
        user1 = self.make_user('user1')
        bd1 = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=user1,
            name='test2',
            content='<xml></xml>'
        )
        sr1 = SupportRequest.objects.create(
            owner=self.admin,
            subject='Help 1',
            body='Foo',
            experience_level=2,
            category='DEBUG',
            program=bd1
        )
        sr2 = SupportRequest.objects.create(
            owner=user1,
            subject='Help 2',
            body='Bar',
            experience_level=2,
            category='WHAT_NEXT',
            program=bd2
        )
        response = self.get(
            reverse('api:v1:supportrequest-list') +
            '?owner=' + str(user1.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()))
        self.assertEqual(response.json()[0]['id'], bd2.id)
        self.assertEqual(response.json()[0]['owner'], user1.id)
        self.assertEqual(response.json()[0]['subject'], sr2.subject)
        self.assertEqual(response.json()[0]['body'], sr2.body)
        self.assertEqual(response.json()[0]['experience_level'], sr2.experience_level)
        self.assertEqual(response.json()[0]['category'], sr2.category)
        self.assertEqual(response.json()[0]['program'], sr2.program.id)

    def test_support_request_not_logged_in(self):
        """Test the support request view denies unauthenticated user."""
        response = self.get(reverse('api:v1:supportrequest-list'))
        self.assertEqual(401, response.status_code)

    def test_support_request_create(self):
        """Test creating support request sets user and in_progress."""
        self.client.login(username='administrator', password='password')
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        data = {
            'subject': 'Help 1',
            'body': 'Foo',
            'experience_level': 2,
            'category': 'DEBUG',
            'program': bd.id
        }
        response = self.client.post(
            reverse('api:v1:supportrequest-list'), data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(SupportRequest.objects.last().owner.id, self.admin.id)
        self.assertEqual(SupportRequest.objects.last().subject, data['subject'])
        self.assertEqual(SupportRequest.objects.last().in_progress, False)

    def test_support_request_update_as_valid_user(self):
        """Test updating support request as owner."""
        self.client.login(username='administrator', password='password')
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        sr = SupportRequest.objects.create(
            owner=self.admin,
            subject='Help 1',
            body='Foo',
            experience_level=2,
            category='DEBUG',
            program=bd
        )
        data = {
            'subject': 'Help New',
        }
        response = self.client.patch(
            reverse(
                'api:v1:supportrequest-detail', kwargs={'pk': sr.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(SupportRequest.objects.last().owner.id, self.admin.id)
        self.assertEqual(SupportRequest.objects.last().subject, data['subject'])

    def test_support_request_update_as_invalid_user(self):
        """Test updating support request as another user."""
        self.client.login(username='administrator', password='password')
        user = self.make_user()
        bd = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        sr = SupportRequest.objects.create(
            owner=user,
            subject='Help 1',
            body='Foo',
            experience_level=2,
            category='DEBUG',
            program=bd
        )
        data = {
            'subject': 'Help New',
        }
        response = self.client.patch(
            reverse(
                'api:v1:supportrequest-detail', kwargs={'pk': sr.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.content,
            b'["You may only modify your own support requests"]')
        self.assertEqual(SupportRequest.objects.last().owner.id, user.id)
        self.assertEqual(SupportRequest.objects.last().subject, 'Help 1')
