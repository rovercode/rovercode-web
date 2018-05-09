"""Blog test views."""
from test_plus.test import TestCase

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rovercode_web.blog.models import Post

from datetime import datetime


class BaseAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Setup the tests."""
        self.nonstaffuser = get_user_model().objects.create_user(
            username='nonstaffuser',
            email='admin@example.com',
            password='password'
        )


class BaseStaffAuthenticatedTestCase(TestCase):
    """Base class for all authenticated test cases."""

    def setUp(self):
        """Setup the tests."""
        self.staff = get_user_model().objects.create_user(
            username='staff',
            email='staff@example.com',
            password='password',
            is_staff=True
        )


class TestPostEditView(BaseStaffAuthenticatedTestCase):
    """Tests the post edit view."""

    def test_post_edit(self):
        """Test the post edit view."""
        self.client.login(username='staff', password='password')
        post = Post.objects.create(
            author=self.staff,
            slug='f1rst-p0st'
        )
        response = self.get(reverse(
            'blog:post_edit',
            kwargs={'slug': post.slug}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, post.slug)

    def test_post_save(self):
        """Test saving a post."""
        self.client.login(username='staff', password='password')
        post = Post.objects.create(
            author=self.staff,
            slug='f1rst-p0st'
        )
        content = {
            'title': 'F1rst P0st',
            'slug': 'f1rst-p0st',
            'author': self.staff.id,
            'content': 'foo',
            'lead': 'bar',
            'published_date': datetime.utcnow(),
            'published': True
        }
        response = self.client.post(
            reverse('blog:post_edit', kwargs={'slug': post.slug}),
            content)
        self.assertRedirects(
            response,
            reverse('blog:post_detail', kwargs={'slug': post.slug}))
        post_obj = Post.objects.get(slug=post.slug)
        self.assertEqual(post_obj.slug, post.slug)
        self.assertEqual(
            post_obj.content, content['content'])
        self.assertEqual(
            post_obj.title, content['title'])
        self.assertEqual(
            post_obj.author, self.staff)
        self.assertEqual(
            post_obj.published_date.replace(tzinfo=None),
            content['published_date'])
        self.assertEqual(
            post_obj.published, content['published'])

    def test_post_save_invalid_form(self):
        """Test saving a post with an invalid form."""
        self.client.login(username='staff', password='password')
        post = Post.objects.create(
            author=self.staff,
            slug='f1rst-p0st'
        )
        content = {}
        response = self.client.post(
            reverse('blog:post_edit', kwargs={'slug': post.slug}),
            content)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "alert alert-danger")
        self.assertContains(response, "This field is required.")

    def test_post_new(self):
        """Test the post edit view for creating a new post."""
        self.client.login(username='staff', password='password')
        response = self.get(reverse('blog:post_new'))
        self.assertEqual(200, response.status_code)

    def test_home_load_nonexistent(self):
        """Test the post edit view trying to load a nonexistent post."""
        self.client.login(username='staff', password='password')
        Post.objects.create(
            author=self.staff,
            slug='f1rst-p0st'
        )
        response = self.get(reverse(
            'blog:post_edit',
            kwargs={'slug': 'some-other-slug'}))
        self.assertEqual(404, response.status_code)

    def test_home_load_nonstaff(self):
        """Test the post edit view trying to load a nonexistent post."""
        self.client.login(username='nonstaffuser', password='password')
        Post.objects.create(
            author=self.staff,
            slug='f1rst-p0st'
        )
        response = self.get(reverse(
            'blog:post_edit',
            kwargs={'slug': 'some-other-slug'}))
        self.assertEqual(302, response.status_code)


class TestPostDetailView(TestCase):
    """Tests the post detail view."""

    def test_post_detail(self):
        """Test the post detail view."""
        user = self.make_user()
        post = Post.objects.create(
            author=user,
            slug='f1rst-p0st'
        )
        response = self.get(reverse(
            'blog:post_detail',
            kwargs={'slug': post.slug}))
        self.assertEqual(200, response.status_code)

    def test_home_load_nonexistent(self):
        """Test the post detail view tring to load a nonexistent post."""
        user = self.make_user()
        Post.objects.create(
            author=user,
            slug='f1rst-p0st'
        )
        response = self.get(reverse(
            'blog:post_detail',
            kwargs={'slug': 'some-other-slug'}))
        self.assertEqual(404, response.status_code)


class TestPostListView(TestCase):
    """Tests the post list view."""

    def test_list(self):
        """Test the post list view displays the correct items."""
        user = self.make_user()
        post1 = Post.objects.create(
            author=user,
            title='Foo',
            slug='foo',
            published=True
        )
        post2 = Post.objects.create(
            author=user,
            title='Bar',
            slug='bar',
            published=True
        )
        response = self.get(reverse('blog:post_list'))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, post1.title)
        self.assertContains(response, post2.title)


class TestPostViewSet(BaseAuthenticatedTestCase):
    """Tests the post API view."""

    def test_post(self):
        """Test the post view displays the correct items."""
        self.client.login(username='nonstaffuser', password='password')
        user = self.make_user()
        Post.objects.create(
            title='Foo',
            slug='foo',
            author=self.nonstaffuser
        )
        Post.objects.create(
            title='Bar',
            slug='bar',
            author=user
        )
        response = self.get(reverse('blog:post-list'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json()))
        self.assertEqual(response.json()[0]['title'], 'Foo')
        self.assertEqual(response.json()[0]['slug'], 'foo')
        self.assertEqual(response.json()[0]['author'], self.nonstaffuser.id)
        self.assertEqual(response.json()[1]['title'], 'Bar')
        self.assertEqual(response.json()[1]['slug'], 'bar')
        self.assertEqual(response.json()[1]['author'], user.id)

    def test_post_fails_non_admin(self):
        """Test the post view doesn't allow new post from non-admin."""
        self.client.login(username='nonstaffuser', password='password')
        user = self.make_user()

        content = {
            'title': 'F1rst P0st',
            'slug': 'f1rst-p0st',
            'author': user.id,
            'content': 'foo',
            'lead': 'bar',
            'published_date': datetime.utcnow(),
            'published': True
        }
        response = self.client.post(reverse('blog:post-list'), content)
        self.assertEqual(403, response.status_code)
