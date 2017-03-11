"""Mission Control models."""
from django.db import models
from rovercode_web.users.models import User


class Rover(models.Model):
    """Attributes to describe a single rover."""

    name = models.TextField()
    owner = models.TextField()
    local_ip = models.TextField()
    last_checkin = models.DateTimeField(auto_now=True)

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
