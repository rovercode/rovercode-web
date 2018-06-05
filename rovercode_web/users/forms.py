"""Users forms."""
from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import filter_users_by_email


class SilentResetPasswordForm(ResetPasswordForm):
    """Does not show an error if the email does not exist in the system."""

    def clean_email(self):
        """Clean email field."""
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)

        return self.cleaned_data["email"]
