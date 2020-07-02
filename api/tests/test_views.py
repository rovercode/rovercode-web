"""API test views."""
from unittest.mock import patch

from test_plus.test import TestCase

import json

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from curriculum.models import Course
from curriculum.models import Lesson
from curriculum.models import ProgressState
from curriculum.models import State
from mission_control.models import BlockDiagram
from mission_control.models import Tag


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

    def authenticate(self, username='administrator', password='password'):
        """Authenticate the test client."""
        credentials = {
            'username': username,
            'password': password,
        }
        response = self.client.post(
            reverse('api:api-token-auth'),
            data=json.dumps(credentials),
            content_type='application/json')

        self.assertEqual(200, response.status_code)

        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(response.json()['token']))


@override_settings(SUPPORT_CONTACT='support@example.com')
class TestBlockDiagramViewSet(BaseAuthenticatedTestCase):
    """Tests the block diagram API view."""

    def setUp(self):
        """Initialize the tests."""
        super().setUp()
        self.support = self.make_user(username='support', password='password')
        self.patcher = patch('requests.post')
        self.mock_post = self.patcher.start()
        self.mock_post.return_value.status_code = 404

    def tearDown(self):
        """Tear down the tests."""
        super().tearDown()
        self.patcher.stop()

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
        # Should not be in the list
        BlockDiagram.objects.create(
            user=self.support,
            name='1 - test',
            content='<xml></xml>'
        )
        response = self.get(reverse('api:v1:blockdiagram-list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(2, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['id'], bd1.id)
        self.assertDictEqual(response.json()['results'][0]['user'], {
            'username': self.admin.username,
        })
        self.assertEqual(response.json()['results'][0]['name'], 'test')
        self.assertEqual(
            response.json()['results'][0]['content'], '<xml></xml>')
        self.assertEqual(response.json()['results'][1]['id'], bd2.id)
        self.assertDictEqual(response.json()['results'][1]['user'], {
            'username': user.username,
        })
        self.assertEqual(response.json()['results'][1]['name'], 'test1')
        self.assertEqual(
            response.json()['results'][1]['content'], '<xml></xml>')

    def test_bd_user_filter(self):
        """Test the block diagram API view filters on user correctly."""
        self.authenticate(username='support')
        BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        bd = BlockDiagram.objects.create(
            user=self.support,
            name='1 - test',
            content='<xml></xml>'
        )
        response = self.get(
            reverse('api:v1:blockdiagram-list') +
            '?user=' + str(self.support.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(1, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['id'], bd.id)
        self.assertDictEqual(response.json()['results'][0]['user'], {
            'username': self.support.username,
        })
        self.assertEqual(response.json()['results'][0]['name'], '1 - test')
        self.assertEqual(
            response.json()['results'][0]['content'], '<xml></xml>')

    def test_bd_user_exclude_filter(self):
        """Test the block diagram API view filters on user exclude correctly."""
        self.authenticate()
        user1 = self.make_user('user1')
        user2 = self.make_user('user2')
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        BlockDiagram.objects.create(
            user=user1,
            name='test2',
            content='<xml></xml>'
        )
        ref = BlockDiagram.objects.create(
            user=user2,
            name='test2',
            content='<xml></xml>'
        )
        course = Course.objects.create(name='Course')
        Lesson.objects.create(
            course=course, sequence_number=1, reference=ref)
        response = self.get(
            reverse('api:v1:blockdiagram-list') +
            '?user__not=' + str(user1.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(1, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['id'], bd.id)
        self.assertDictEqual(response.json()['results'][0]['user'], {
            'username': self.admin.username,
        })
        self.assertEqual(response.json()['results'][0]['name'], 'test1')
        self.assertEqual(
            response.json()['results'][0]['content'], '<xml></xml>')

    def test_bd_not_logged_in(self):
        """Test the block diagram view denies unauthenticated user."""
        response = self.get(reverse('api:v1:blockdiagram-list'))
        self.assertEqual(401, response.status_code)

    def test_bd_create(self):
        """Test creating block diagram sets user."""
        self.authenticate()
        data = {
            'name': 'test',
            'content': '<xml></xml>',
            'owner_tags': ['tag1', 'tag 2'],
        }
        response = self.client.post(
            reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, data['name'])
        model_tags = [t.name for t in BlockDiagram.objects.last().tags.all()]
        self.assertIn('tag1', model_tags)
        self.assertIn('tag 2', model_tags)

    def test_bd_create_name_exist(self):
        """Test creating block diagram when name already exists."""
        BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )

        self.authenticate()
        data = {
            'name': 'test',
            'content': '<xml></xml>'
        }
        response = self.client.post(
            reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(
            BlockDiagram.objects.last().name, data['name'] + ' (1)')

    def test_bd_create_name_exist_with_number(self):
        """Test creating block diagram when name already exists with number."""
        user1 = self.make_user('user1')
        BlockDiagram.objects.create(
            user=self.admin,
            name='test (1) (2)',
            content='<xml></xml>'
        )
        BlockDiagram.objects.create(
            user=user1,
            name='test (1) (3)',
            content='<xml></xml>'
        )

        self.authenticate()
        data = {
            'name': 'test (1) (2)',
            'content': '<xml></xml>'
        }
        response = self.client.post(
            reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test (1) (3)')

    def test_bd_update_as_valid_user(self):
        """Test updating block diagram as owner."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        course = Course.objects.create(name='Course')
        lesson = Lesson.objects.create(
            course=course, sequence_number=1, reference=bd)
        data = {
            'name': 'test',
            'lesson': lesson.id,
        }
        response = self.client.patch(
            reverse(
                'api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test')
        self.assertEqual(BlockDiagram.objects.last().lesson, lesson)

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
        self.assertEqual(404, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, user.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test1')

    def test_bd_delete_as_valid_user(self):
        """Test deleting block diagram as owner."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test1',
            content='<xml></xml>'
        )
        response = self.client.delete(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
        )
        self.assertEqual(204, response.status_code)
        self.assertFalse(BlockDiagram.objects.filter(id=bd.id).exists())

    def test_bd_delete_as_invalid_user(self):
        """Test deleting block diagram as another user."""
        self.authenticate()
        user = self.make_user()
        bd = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        response = self.client.delete(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, user.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test1')

    def test_bd_update_add_tags(self):
        """Test updating block diagram to add tags."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>',
        )
        self.assertEqual(0, BlockDiagram.objects.get(id=bd.id).tags.count())

        # Add the tag
        data = {
            'owner_tags': ['test'],
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test')
        self.assertEqual(1, BlockDiagram.objects.last().tags.count())

        response = self.client.get(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('test', response.data['tags'])

    def test_bd_update_remove_tags(self):
        """Test updating block diagram to remove tags."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>',
        )
        tag = Tag.objects.create(name='tag1')
        bd.owner_tags.add(tag)
        self.assertEqual(1, BlockDiagram.objects.get(id=bd.id).tags.count())

        # Remove the tag
        data = {
            'owner_tags': [],
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(BlockDiagram.objects.last().user.id, self.admin.id)
        self.assertEqual(BlockDiagram.objects.last().name, 'test')
        self.assertEqual(0, BlockDiagram.objects.last().tags.count())

    def test_bd_update_add_tag_too_long(self):
        """Test updating block diagram to add tag that is too long."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>',
        )
        self.assertEqual(0, BlockDiagram.objects.get(id=bd.id).tags.count())

        # Add the tag
        data = {
            'owner_tags': ['a'*100],
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, BlockDiagram.objects.get(id=bd.id).tags.count())

    def test_bd_update_add_tag_too_short(self):
        """Test updating block diagram to add tag that is too short."""
        self.authenticate()
        bd = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>',
        )
        self.assertEqual(0, BlockDiagram.objects.get(id=bd.id).tags.count())

        # Add the tag
        data = {
            'owner_tags': ['a'],
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.pk}),
            json.dumps(data), content_type='application/json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(0, BlockDiagram.objects.get(id=bd.id).tags.count())

    def test_bd_tag_filter(self):
        """Test the block diagram API view filters on tags correctly."""
        self.authenticate()
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
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        tag3 = Tag.objects.create(name='tag3')
        tag4 = Tag.objects.create(name='tag4')
        bd1.owner_tags.set([tag1, tag2])
        bd1.admin_tags.add(tag3)
        bd2.owner_tags.add(tag4)
        bd2.admin_tags.add(tag3)

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?tag={},{}'.format(
                tag1.name, tag2.name))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(1, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['id'], bd1.id)
        self.assertDictEqual(response.json()['results'][0]['user'], {
            'username': self.admin.username,
        })
        self.assertEqual(response.json()['results'][0]['name'], 'test1')
        self.assertEqual(
            response.json()['results'][0]['content'], '<xml></xml>')

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?tag=' + tag3.name)

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(2, len(response.json()['results']))

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?tag={},{}'.format(
                tag2.name, tag3.name))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(2, len(response.json()['results']))

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?owner_tags={},{}'.format(
                tag4.name, tag3.name))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(1, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['name'], 'test2')

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?admin_tags={}'.format(
                tag3.name))

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(2, len(response.json()['results']))

        response = self.get(
            reverse('api:v1:blockdiagram-list') + '?tag=' + 'nothing')

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(0, len(response.json()['results']))

    def test_profanity_check(self):
        """Test that email is sent when profanity detected."""
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.return_value = {
            'censored': 'profane-word',
            'original_profane_word': 'profane-word',
            'uncensored': 'profane-word',
        }

        self.assertEqual(0, len(mail.outbox))

        self.authenticate()
        data = {
            'name': 'profane-word',
            'content': '<xml></xml>',
        }
        response = self.client.post(reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)

        self.assertEqual(1, len(mail.outbox))
        self.assertIn(self.admin.username, mail.outbox[0].body)
        self.assertIn('profane-word', mail.outbox[0].body)

    @patch('mission_control.signals.handlers.LOGGER')
    def test_profanity_check_failure(self, mock_logger):
        """Test that error is logged if unable to contact profanity check."""
        self.assertEqual(0, len(mail.outbox))

        self.authenticate()
        data = {
            'name': 'profane-word',
            'content': '<xml></xml>',
        }
        response = self.client.post(reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)

        self.assertEqual(0, len(mail.outbox))
        self.assertTrue(mock_logger.error.called)
        self.assertEqual(404, mock_logger.error.call_args[0][1])

    def test_profanity_check_flag(self):
        """Test that program is flagged correctly."""
        profane_response = {
            'censored': 'profane-word',
            'original_profane_word': 'profane-word',
            'uncensored': 'profane-word',
        }
        normal_response = {
            'censored': 'word',
            'original_profane_word': None,
            'uncensored': 'word',
        }
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.json.side_effect = [
            profane_response,
            normal_response,
            profane_response,
        ]

        self.assertEqual(0, len(mail.outbox))

        self.authenticate()
        data = {
            'name': 'profane-word',
            'content': '<xml></xml>',
        }
        response = self.client.post(reverse('api:v1:blockdiagram-list'), data)
        self.assertEqual(201, response.status_code)

        bd = BlockDiagram.objects.first()
        self.assertTrue(bd.flagged)

        data = {
            'name': 'word',
            'content': '<xml></xml>',
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.id}), data)
        self.assertEqual(200, response.status_code)

        bd = BlockDiagram.objects.first()
        self.assertFalse(bd.flagged)

        data = {
            'name': 'profane-word',
            'content': '<xml></xml>',
        }
        response = self.client.patch(
            reverse('api:v1:blockdiagram-detail', kwargs={'pk': bd.id}), data)
        self.assertEqual(200, response.status_code)

        bd = BlockDiagram.objects.first()
        self.assertTrue(bd.flagged)

    def test_remix(self):
        """Test remixing a block diagram."""
        self.authenticate()
        user = self.make_user()
        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        response = self.post(
            reverse('api:v1:blockdiagram-remix', kwargs={'pk': bd1.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response.json()['user']['username'], self.admin.username)
        self.assertEqual(response.json()['name'], bd1.name)
        self.assertEqual(response.json()['content'], bd1.content)
        self.assertIsNone(response.json()['lesson'])
        self.assertIsNone(response.json()['state'])

    def test_remix_reference(self):
        """Test remixing a reference block diagram."""
        self.authenticate()
        user = self.make_user()
        course = Course.objects.create(name='Test')
        bd = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        Lesson.objects.create(
            reference=bd, sequence_number=1, course=course)
        response = self.post(
            reverse('api:v1:blockdiagram-remix', kwargs={'pk': bd.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response.json()['user']['username'], self.admin.username)
        self.assertEqual(response.json()['name'], bd.name)
        self.assertEqual(response.json()['content'], bd.content)
        self.assertEqual(response.json()['lesson'], bd.reference_of.id)
        self.assertDictEqual(response.json()['state'], {
            'progress': 'IN_PROGRESS',
        })

    def test_remix_unknown(self):
        """Test remixing an unknown block diagram."""
        self.authenticate()
        response = self.post(
            reverse('api:v1:blockdiagram-remix', kwargs={'pk': 100}))
        self.assertEqual(404, response.status_code)

    def test_remix_own(self):
        """Test remixing own block diagram."""
        self.authenticate()
        bd1 = BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )
        response = self.post(
            reverse('api:v1:blockdiagram-remix', kwargs={'pk': bd1.id}))
        self.assertEqual(400, response.status_code)

    def test_remix_again(self):
        """Test remixing block diagram already remixed."""
        self.authenticate()
        user = self.make_user()
        BlockDiagram.objects.create(
            user=self.admin,
            name='test',
            content='<xml></xml>'
        )
        BlockDiagram.objects.create(
            user=self.admin,
            name='test (1)',
            content='<xml></xml>'
        )
        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        response = self.post(
            reverse('api:v1:blockdiagram-remix', kwargs={'pk': bd1.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response.json()['user']['username'], self.admin.username)
        self.assertEqual(response.json()['name'], f'{bd1.name} (2)')
        self.assertEqual(response.json()['content'], bd1.content)
        self.assertIsNone(response.json()['lesson'])
        self.assertIsNone(response.json()['state'])

    def test_report(self):
        """Test reporting a block diagram."""
        self.authenticate()
        user = self.make_user()

        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        self.assertEqual(
            0, BlockDiagram.objects.filter(user=self.support).count())
        self.assertEqual(0, len(mail.outbox))

        data = {
            'description': 'Something went wrong',
        }
        response = self.post(
            reverse('api:v1:blockdiagram-report', kwargs={'pk': bd1.id}),
            data=data
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            1, BlockDiagram.objects.filter(user=self.support).count())
        self.assertEqual(
            f'{bd1.id} - test',
            BlockDiagram.objects.filter(user=self.support).last().name
        )
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('Something went wrong', mail.outbox[0].body)
        self.assertIn(f'{bd1.id}:{bd1.name}', mail.outbox[0].body)

    def test_report_again(self):
        """Test reporting a block diagram already reported."""
        self.authenticate()
        user = self.make_user()

        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        BlockDiagram.objects.create(
            user=self.support,
            name=f'{bd1.id} - test',
            content='<xml></xml>'
        )
        self.assertEqual(
            1, BlockDiagram.objects.filter(user=self.support).count())
        self.assertEqual(0, len(mail.outbox))

        data = {
            'description': 'Something went wrong',
        }
        response = self.post(
            reverse('api:v1:blockdiagram-report', kwargs={'pk': bd1.id}),
            data=data
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            2, BlockDiagram.objects.filter(user=self.support).count())
        self.assertEqual(
            f'{bd1.id} - test (1)',
            BlockDiagram.objects.filter(user=self.support).last().name
        )
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('Something went wrong', mail.outbox[0].body)
        self.assertIn(f'{bd1.id}:{bd1.name}', mail.outbox[0].body)


class TestUserViewSet(BaseAuthenticatedTestCase):
    """Tests the user API view."""

    def test_modify(self):
        """Test modifying user."""
        self.authenticate()

        self.assertTrue(
            get_user_model().objects.get(id=self.admin.id).show_guide)

        data = {
            'show_guide': False,
        }
        response = self.client.put(reverse('api:v1:user-detail', kwargs={
            'pk': self.admin.pk,
        }), data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(
            get_user_model().objects.get(id=self.admin.id).show_guide)

    def test_modify_other(self):
        """Test modifying other user."""
        self.authenticate()
        user = self.make_user()

        self.assertTrue(
            get_user_model().objects.get(id=self.admin.id).show_guide)

        data = {
            'show_guide': False,
        }
        response = self.client.put(reverse('api:v1:user-detail', kwargs={
            'pk': user.pk,
        }), data)
        self.assertEqual(400, response.status_code)
        self.assertTrue(
            get_user_model().objects.get(id=self.admin.id).show_guide)


class TestCourseViewSet(BaseAuthenticatedTestCase):
    """Tests the course API view."""

    def setUp(self):
        """Initialize the tests."""
        super().setUp()
        self.patcher = patch('requests.post')
        self.mock_post = self.patcher.start()
        self.mock_post.return_value.status_code = 404

    def tearDown(self):
        """Tear down the tests."""
        super().tearDown()
        self.patcher.stop()

    def test_course_list(self):
        """Test listing courses."""
        self.authenticate()
        user = self.make_user()
        bd1 = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
        )
        bd2 = BlockDiagram.objects.create(
            user=user,
            name='test1',
            content='<xml></xml>'
        )
        course1 = Course.objects.create(name='Course1')
        course2 = Course.objects.create(name='Course2')
        lesson1 = Lesson.objects.create(
            course=course1,
            sequence_number=1,
            reference=bd1,
            tutorial_link='https://lesson1.test/',
            goals='Lesson 1 goals',
        )
        lesson2 = Lesson.objects.create(
            course=course2,
            sequence_number=2,
            reference=bd2,
            tutorial_link='https://lesson2.test/',
            goals='Lesson 2 goals',
        )

        state = State.objects.create(progress=ProgressState.COMPLETE)
        bd3 = BlockDiagram.objects.create(
            user=self.admin,
            name='remix',
            content='<xml></xml>',
            lesson=lesson2,
            state=state
        )

        response = self.client.get(reverse('api:v1:course-list'))
        self.assertEqual(200, response.status_code)

        self.assertEqual(1, response.json()['total_pages'])
        self.assertEqual(2, len(response.json()['results']))
        self.assertEqual(response.json()['results'][0]['id'], course1.id)
        self.assertEqual(response.json()['results'][0]['name'], course1.name)
        self.assertEqual(1, len(response.json()['results'][0]['lessons']))
        self.assertDictEqual(response.json()['results'][0]['lessons'][0], {
            'id': lesson1.id,
            'reference': lesson1.reference.name,
            'course': course1.name,
            'description': lesson1.reference.description,
            'sequence_number': lesson1.sequence_number,
            'active_bd': lesson1.reference.pk,
            'active_bd_owned': False,
            'state': None,
            'tutorial_link': lesson1.tutorial_link,
            'goals': lesson1.goals,
        })

        self.assertEqual(response.json()['results'][1]['id'], course2.id)
        self.assertEqual(response.json()['results'][1]['name'], course2.name)
        self.assertEqual(1, len(response.json()['results'][1]['lessons']))
        self.assertDictEqual(response.json()['results'][1]['lessons'][0], {
            'id': lesson2.id,
            'reference': lesson2.reference.name,
            'course': course2.name,
            'description': lesson2.reference.description,
            'sequence_number': lesson2.sequence_number,
            'active_bd': bd3.pk,
            'active_bd_owned': True,
            'tutorial_link': lesson2.tutorial_link,
            'goals': lesson2.goals,
            'state': {
                'progress': state.progress.name,
            },
        })
