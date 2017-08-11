"""Blog test urls."""
from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestBlogURLs(TestCase):
    """Tests the urls."""

    def test_posts_list_reverse(self):
        """blog:post_list should reverse to /blog/."""
        self.assertEqual(reverse('blog:post_list'), '/blog/')

    def test_posts_resolve(self):
        """/blog/ should resolve to blog:post_list."""
        self.assertEqual(
            resolve('/blog/').view_name,
            'blog:post_list')

    def test_drafts_list_reverse(self):
        """blog:post_drafts_list should reverse to /blog/post-drafts-list/."""
        self.assertEqual(
            reverse('blog:post_drafts_list'), '/blog/post-drafts-list/')

    def test_drafts_list_resolve(self):
        """/blog/post-drafts-list/ should resolve to blog:post_drafts_list."""
        self.assertEqual(
            resolve('/blog/post-drafts-list/').view_name,
            'blog:post_drafts_list')

    def test_post_edit_load_reverse(self):
        """blog:post_edit should reverse to /blog/post-edit/f1rst-p0st."""
        self.assertEqual(
            reverse('blog:post_edit', kwargs={'slug': 'f1rst-p0st'}),
            '/blog/post-edit/f1rst-p0st/')

    def test_post_edit_load_resolve(self):
        """/blog/post-edit/f1rst-p0st should resolve to blog:post_edit."""
        match = resolve('/blog/post-edit/f1rst-p0st/')
        self.assertEqual(match.view_name, 'blog:post_edit')
        self.assertEqual(match.kwargs['slug'], 'f1rst-p0st')

    def test_post_new_load_reverse(self):
        """blog:post_new should reverse to /blog/post-edit/."""
        self.assertEqual(
            reverse('blog:post_new'),
            '/blog/post-edit/')

    def test_post_new_load_resolve(self):
        """/blog/post-edit/ should resolve to blog:post_new."""
        match = resolve('/blog/post-edit/')
        self.assertEqual(match.view_name, 'blog:post_new')

    def test_post_detail_load_reverse(self):
        """blog:post_detail should reverse to /blog/post-detail/f1rst-p0st."""
        self.assertEqual(
            reverse('blog:post_detail', kwargs={'slug': 'f1rst-p0st'}),
            '/blog/post-detail/f1rst-p0st/')

    def test_post_detail_load_resolve(self):
        """/blog/post-detail/f1rst-p0st should resolve to blog:post_detail."""
        match = resolve('/blog/post-detail/f1rst-p0st/')
        self.assertEqual(match.view_name, 'blog:post_detail')
        self.assertEqual(match.kwargs['slug'], 'f1rst-p0st')

    def test_block_diagrams_reverse(self):
        """blog:post-list should reverse to /blog/posts/."""  # noqa
        self.assertEqual(
            reverse('blog:post-list'),
            '/blog/posts/')

    def test_block_diagrams_resolve(self):
        """/blog/posts/ should resolve to blog:post-list."""  # noqa
        self.assertEqual(
            resolve('/blog/posts/').view_name,
            'blog:post-list')
