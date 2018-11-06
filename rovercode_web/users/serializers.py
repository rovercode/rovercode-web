"""User serializers."""
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = ('id', 'blocked_users')
        read_only_fields = ('password', 'last_login', 'is_superuser',
                            'username', 'first_name', 'last_name',
                            'email', 'is_staff', 'is_active', 'date_joined',
                            'name', 'groups', 'user_permissions',)
