"""Mission Control apps."""
from django.apps import AppConfig


class MissionControlConfig(AppConfig):
    """Configuration for the Mission Control app."""

    name = 'mission_control'

    def ready(self):
        """Run operations required after app is loaded."""
        import mission_control.signals.handlers  # noqa
