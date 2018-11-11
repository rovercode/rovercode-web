"""Support models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from oauth2_provider.models import Application
from rovercode_web.users.models import User
from mission_control.models import BlockDiagram


class SupportRequest(models.Model):
    CATEGORIES = (
        ("DEBUG", "DEBUG"),
        ("WHAT_NEXT", "WHAT_NEXT"),
        ("FUN_IDEAS", "FUN_IDEAS"),
    )

    """Attributes to describe a single support request."""
    subject = models.CharField(null=False, max_length=25)
    body = models.CharField(null=False, max_length=2000)
    experience_level = models.IntegerField(null=False, validators=[MinValueValidator(0), MaxValueValidator(3)])
    category = models.CharField(null=False, max_length=25, choices=CATEGORIES)
    owner = models.ForeignKey(User)
    creation_time = models.DateTimeField(auto_now=True)
    in_progress = models.BooleanField(null=False, default=False)
    program = models.ForeignKey(BlockDiagram)

    class Meta:
        """Meta class."""

    def __str__(self):
        """Convert the model to a human readable string."""
        return "Support Request {}: {}".format(self.id, self.subject)


class AbuseReport(models.Model):
    """Attributes to describe a single abuse report."""
    reporter = models.ForeignKey(User, related_name='reporter')
    accused_user = models.ForeignKey(User, null=True, related_name='accused_user')
    support_request = models.ForeignKey(SupportRequest)
    transcript = models.CharField(null=False, max_length=100000)
    creation_time = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

    def __str__(self):
        """Convert the model to a human readable string."""
        return "Abuse Report {}: User {} against {}".format(self.id, self.reporter, self.accused_user)
