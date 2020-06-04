"""Mission Control test handlers."""
import json
from unittest.mock import Mock
from unittest.mock import patch

from test_plus.test import TestCase

from mission_control.handlers import SumoHandler


class TestSumoHandler(TestCase):
    """Tests sumologic logging handler."""

    def setUp(self):
        """Initialize the tests."""
        super().setUp()
        self.patcher = patch('requests.post')
        self.mock_post = self.patcher.start()
        self.mock_post.return_value.status_code = 404

        self.user = self.make_user()

    def tearDown(self):
        """Tear down the tests."""
        super().tearDown()
        self.patcher.stop()

    def test_log(self):
        """Test log is sent."""
        data = {
            'event': 'remix',
            'userId': 1,
            'sourceProgramId': 100,
            'newProgramId': 200,
        }
        record = Mock()
        record.getMessage.return_value = json.dumps(data)

        handler = SumoHandler(host='fake.com', url='/not/real/')

        handler.emit(record)

        self.assertEqual(
            'https://fake.com/not/real/', self.mock_post.call_args[0][0])
        self.assertDictEqual(data, self.mock_post.call_args[1]['json'])

    @patch.object(SumoHandler, 'handleError')
    def test_log_error(self, mock_handle):
        """Test handling error sending log."""
        record = Mock()
        record.getMessage.side_effect = IOError()

        handler = SumoHandler(host='fake.com', url='/not/real/')

        handler.emit(record)

        self.assertTrue(mock_handle.called)
