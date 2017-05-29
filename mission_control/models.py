"""Mission Control models."""
from django.db import models
from rovercode_web.users.models import User


class Rover(models.Model):
    """Attributes to describe a single rover."""

    name = models.TextField()
    owner = models.TextField()
    local_ip = models.TextField()
    last_checkin = models.DateTimeField(auto_now=True)
    left_forward_pin = models.TextField(null=False, default='XIO-P0')
    left_backward_pin = models.TextField(null=False, default='XIO-P1')
    right_forward_pin = models.TextField(null=False, default='XIO-P6')
    right_backward_pin = models.TextField(null=False, default='XIO-P7')
    left_eye_pin = models.TextField(null=False, default='XIO-P2')
    right_eye_pin = models.TextField(null=False, default='XIO-P4')

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
