"""Curriculum models."""
from enum import IntEnum

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    """Attributes to describe a single course."""

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        """Convert the model to a human readable string."""
        return self.name


class Lesson(models.Model):
    """Attributes to describe a single lesson."""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons')
    reference = models.OneToOneField(
        'mission_control.BlockDiagram',
        on_delete=models.CASCADE,
        related_name='reference_of')
    sequence_number = models.PositiveSmallIntegerField()
    tutorial_link = models.URLField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)

    def __str__(self):
        """Convert the model to a human readable string."""
        return '{}:{}'.format(self.course.name, self.reference.name)


class ProgressState(IntEnum):
    """Enumeration of all the possible progress states."""

    AVAILABLE = 1
    UNAVAILABLE = 2
    IN_PROGRESS = 3
    COMPLETE = 4

    @classmethod
    def choices(cls):
        """Generate the choices."""
        return [(key.value, key.name) for key in cls]


class State(models.Model):
    """Attributes to describe the state of a lesson."""

    progress = models.SmallIntegerField(
        choices=ProgressState.choices(), default=ProgressState.AVAILABLE)
