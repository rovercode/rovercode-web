"""Mission Control models."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from oauth2_provider.models import Application

User = get_user_model()


class Rover(models.Model):
    """Attributes to describe a single rover."""

    name = models.CharField(null=False, max_length=25)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_application = models.ForeignKey(
        Application, blank=True, null=True, on_delete=models.SET_NULL)
    local_ip = models.CharField(max_length=15, null=True)
    last_checkin = models.DateTimeField(auto_now=True)
    config = JSONField(blank=True, default=dict)
    shared_users = models.ManyToManyField(
        User, related_name='shared_rovers', blank=True)

    class Meta:
        """Meta class."""

        # Don't allow a user to use the same rover name
        unique_together = ('owner', 'name',)

    # pylint: disable=arguments-differ
    def save(self, *args, **kwargs):
        """Set the default config and save the Rover."""
        if self.config == {}:
            self.config = settings.DEFAULT_ROVER_CONFIG
        super().save(*args, **kwargs)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name


class BlockDiagram(models.Model):
    """Attributes to describe a single block diagram."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    content = models.TextField()

    class Meta:
        """Meta class."""

        # Don't allow a user to use the same rover name
        unique_together = ('user', 'name',)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name
