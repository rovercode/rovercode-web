"""Mission Control fields."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from mission_control.models import Tag

User = get_user_model()


class TagStringRelatedField(serializers.StringRelatedField):
    """Custom field to allow for using tag strings in related fields."""

    def to_internal_value(self, data):
        """Convert a tag string into the primary key for the tag."""
        if len(data) < 3:
            raise serializers.ValidationError(
                'Tags must be at least 3 characters')
        elif len(data) > 30:
            raise serializers.ValidationError(
                'Tags must be at most 30 characters')

        tag, _ = Tag.objects.get_or_create(name=data)
        return tag.pk
