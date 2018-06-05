"""Form tests."""
from test_plus.test import TestCase

from ..forms import SilentResetPasswordForm


class TestForms(TestCase):
    """Tests the forms."""

    def test_silent_reset_password_form(self):
        """Tests the silent reset password form."""
        data = {
            'email': 'notauser@example.com'
        }
        form = SilentResetPasswordForm(data)

        self.assertTrue(form.is_valid())
