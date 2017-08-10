"""Blog models."""
from django.db import models
from rovercode_web.users.models import User


class Post(models.Model):
    """Attributes to describe a single blog post."""

    title = models.CharField(null=False, max_length=200)
    slug = models.SlugField(null=False, max_length=100, unique=True)
    author = models.ForeignKey(User)
    lead = models.TextField()
    content = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        """Represent the model with a human readable string."""
        return "\"{}\" by {}".format(self.title, self.author)
