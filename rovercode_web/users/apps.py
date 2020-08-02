"""Users apps."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users application configuration."""

    name = 'rovercode_web.users'
    verbose_name = "Users"

    def ready(self):
        """Run operations required after app is loaded."""
        import rovercode_web.users.signals.handlers  # noqa
