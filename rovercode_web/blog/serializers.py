"""Blog serializers."""
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    class Meta:
        """Meta class."""

        model = Post
        fields = '__all__'
