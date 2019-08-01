"""Mission Control fields."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsernameStringRelatedField(serializers.StringRelatedField):
    """Custom field to allow for using username in related fields."""

    def to_internal_value(self, data):
        """Convert a username into the primary key for the user."""
        try:
            return User.objects.get(username=data).pk
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with username: {} not found'.format(data))
