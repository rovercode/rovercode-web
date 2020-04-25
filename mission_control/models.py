"""Mission Control models."""
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import CICharField
from django.db import models

User = get_user_model()


class BlockDiagram(models.Model):
    """Attributes to describe a single block diagram."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    admin_tags = models.ManyToManyField(
        'Tag', related_name='admin_block_diagrams', blank=True)
    owner_tags = models.ManyToManyField(
        'Tag', related_name='owner_block_diagrams', blank=True)
    flagged = models.BooleanField(default=False)
    lesson = models.ForeignKey(
        'curriculum.Lesson', on_delete=models.SET_NULL, blank=True, null=True,
        related_name='block_diagrams')
    state = models.ForeignKey(
        'curriculum.State', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        """Meta class."""

        # Don't allow a user to use the same rover name
        unique_together = ('user', 'name',)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name

    @property
    def tags(self):
        """All tags for the block diagram."""
        return (self.admin_tags.all() | self.owner_tags.all()).distinct()


class Tag(models.Model):
    """Descriptor to add to another model."""

    name = CICharField(max_length=30, unique=True)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name
