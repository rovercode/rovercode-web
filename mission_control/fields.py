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
        if len(data) > 30:
            raise serializers.ValidationError(
                'Tags must be at most 30 characters')

        tag, _ = Tag.objects.get_or_create(name=data)
        return tag.pk


class UserStringRelatedField(serializers.StringRelatedField):
    """Custom field to allow for using username strings in related fields."""

    def to_internal_value(self, data):
        """Convert username string into the the primary key for the user."""
        try:
            user = User.objects.get(username=data)
        except User.DoesNotExist as e:
            raise serializers.ValidationError(
                f'User \'{data}\' does not exist') from e

        return user.pk


class StringChoiceField(serializers.ChoiceField):
    """Custom field to allow for using friendly string for choice field."""

    def to_representation(self, value):
        """Convert the choice value into the friendly string."""
        return self._choices[value]

    # pylint: disable=inconsistent-return-statements
    def to_internal_value(self, data):
        """Convert string into the choice value."""
        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)
