"""Mission Control models."""
import json

from django.contrib.postgres.fields import JSONField
from django.db import models
from oauth2_provider.models import Application
from rovercode_web.users.models import User


class Rover(models.Model):
    """Attributes to describe a single rover."""

    DEFAULT_CONFIG = {
        'left_eye_port': 1,
        'right_eye_port': 2,
        'left_motor_port': 3,
        'right_motor_port': 4
    }

    name = models.CharField(null=False, max_length=25)
    owner = models.ForeignKey(User)
    oauth_application = models.ForeignKey(Application, blank=True, null=True)
    local_ip = models.CharField(max_length=15, null=True)
    last_checkin = models.DateTimeField(auto_now=True)
    config = JSONField(default=json.dumps(DEFAULT_CONFIG))

    class Meta:
        """Meta class."""

        # Don't allow a user to use the same rover name
        unique_together = ('owner', 'name',)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name


class BlockDiagram(models.Model):
    """Attributes to describe a single block diagram."""

    user = models.ForeignKey(User)
    name = models.TextField()
    content = models.TextField()

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name
