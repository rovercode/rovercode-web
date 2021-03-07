"""Mission Control test models."""
from unittest.mock import patch

from test_plus.test import TestCase

from mission_control.models import BlockDiagram
from mission_control.models import BlockDiagramBlogQuestion
from mission_control.models import BlogQuestion


class BaseBlockDiagramTestCase(TestCase):
    """Base class to initialize the tests."""

    def setUp(self):
        """Initialize the tests."""
        super().setUp()
        self.patcher = patch('requests.post')
        self.mock_post = self.patcher.start()
        self.mock_post.return_value.status_code = 404

        self.user = self.make_user()
        self.bd = BlockDiagram.objects.create(
            user=self.user,
            name='test',
            content='<xml></xml>'
        )

    def tearDown(self):
        """Tear down the tests."""
        super().tearDown()
        self.patcher.stop()


class TestBlockDiagram(BaseBlockDiagramTestCase):
    """Tests the block diagram model."""

    def test__str__(self):
        """Test the stringify method."""
        self.assertEqual(str(self.bd), 'test')

    def test_bd(self):
        """Test the model."""
        self.assertEqual(1, BlockDiagram.objects.count())
        self.assertEqual(self.user.id, BlockDiagram.objects.first().user.id)


class TestBlockDiagramBlogQuestion(BaseBlockDiagramTestCase):
    """Tests the block diagram blog question model."""

    def test__str__(self):
        """Test the stringify method."""
        bq = BlogQuestion.objects.create(question='How did you do it?')
        bdbq = BlockDiagramBlogQuestion.objects.create(
            block_diagram=self.bd,
            blog_question=bq,
            required=True
        )
        self.assertEqual(str(bdbq), 'test: How did you do it?')
