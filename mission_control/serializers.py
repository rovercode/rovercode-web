"""Mission Control serializers."""
import re

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework import serializers
from oauth2_provider.models import Application

from .models import Rover, BlockDiagram

NAME_REGEX = re.compile(r'\((?P<number>\d)\)$')


class RoverSerializer(serializers.ModelSerializer):
    """Rover model serializer."""

    client_id = serializers.CharField(
        source='oauth_application.client_id',
        read_only=True)
    client_secret = serializers.CharField(
        source='oauth_application.client_secret',
        read_only=True)

    class Meta:
        """Meta class."""

        model = Rover
        fields = (
            'id', 'name', 'owner', 'local_ip', 'last_checkin',
            'config', 'client_id', 'client_secret'
        )
        read_only_fields = ('owner',)

    def create(self, validated_data):
        """Create an oauth application when the Rover is created."""
        owner = validated_data.get('owner')
        name = validated_data.get('name')

        oauth_application = Application.objects.create(
            user=owner,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_type=Application.CLIENT_CONFIDENTIAL,
            name=name
        )
        try:
            return Rover.objects.create(oauth_application=oauth_application,
                                        **validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                'There is already a rover with that name')


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = get_user_model()
        fields = ('username', )


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    user = UserSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'

    def create(self, validated_data):
        """Check for name conflict and create unique name if necessary."""
        name = validated_data['name']
        match = NAME_REGEX.search(name)
        if match:
            number = int(match.group('number'))
        else:
            number = None

        user = self.context['request'].user
        while BlockDiagram.objects.filter(name=name, user=user).exists():
            if number is None:
                number = 1
                name = '{} ({})'.format(name, number)
            else:
                number += 1
                name = re.sub(NAME_REGEX, '({})'.format(number), name)

        validated_data['name'] = name
        return super().create(validated_data)
