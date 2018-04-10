"""Mission Control models."""
from django.db import models
from rovercode_web.users.models import User
from oauth2_provider.models import Application


class Rover(models.Model):
    """Attributes to describe a single rover."""

    name = models.CharField(null=False, max_length=25)
    owner = models.ForeignKey(User)
    oauth_application = models.ForeignKey(Application, blank=True, null=True)
    local_ip = models.CharField(max_length=15)
    last_checkin = models.DateTimeField(auto_now=True)
    left_forward_pin = models.CharField(
        null=False, default='XIO-P0', max_length=25)
    left_backward_pin = models.CharField(
        null=False, default='XIO-P1', max_length=25)
    right_forward_pin = models.CharField(
        null=False, default='XIO-P6', max_length=25)
    right_backward_pin = models.CharField(
        null=False, default='XIO-P7', max_length=25)
    left_eye_pin = models.CharField(
        null=False, blank=True, default='XIO-P2', max_length=25)
    right_eye_pin = models.CharField(
        null=False, blank=True, default='XIO-P4', max_length=25)
    right_eye_i2c_port = models.IntegerField(
        null=False, blank=True, default=1)
    right_eye_i2c_addr = models.IntegerField(
        null=False, blank=True, default=19)
    left_eye_i2c_port = models.IntegerField(
        null=False, blank=True, default=2)
    left_eye_i2c_addr = models.IntegerField(
        null=False, blank=True, default=19)

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
