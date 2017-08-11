"""Blog test models."""
from test_plus.test import TestCase

from rovercode_web.blog.models import Post


class TestPost(TestCase):
    """Tests the Post model."""

    def test__str__(self):
        """Test the stringify method."""
        user = self.make_user()
        self.post = Post.objects.create(
            title='F1rst P0st',
            author=user,
        )
        self.assertEqual(str(self.post), '"F1rst P0st" by testuser')
