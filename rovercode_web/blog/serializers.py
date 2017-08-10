"""Blog serializers."""
from .models import Post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    class Meta:
        """Meta class."""

        model = Post
        fields = '__all__'
