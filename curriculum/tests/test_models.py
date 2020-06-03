"""Curriculum test models."""
from unittest.mock import patch

from test_plus.test import TestCase

from curriculum.models import Course
from curriculum.models import Lesson
from curriculum.models import ProgressState
from curriculum.models import State
from mission_control.models import BlockDiagram


class TestCourse(TestCase):
    """Tests the course model."""

    def test__str__(self):
        """Test the stringify method."""
        course = Course.objects.create(name='Test')
        self.assertEqual(str(course), 'Test')


class TestLesson(TestCase):
    """Tests the lesson model."""

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

    def test__str__(self):
        """Test the stringify method."""
        course = Course.objects.create(name='Test')
        user = self.make_user()
        bd = BlockDiagram.objects.create(
            user=user,
            name='ref',
            content='<xml></xml>'
        )
        lesson = Lesson.objects.create(
            reference=bd, sequence_number=1, course=course)
        self.assertEqual(str(lesson), 'Test:ref')


class TestState(TestCase):
    """Tests the state model."""

    def test_default(self):
        """Test the default progress state."""
        State.objects.create()
        self.assertEqual(
            State.objects.first().progress, ProgressState.AVAILABLE)
