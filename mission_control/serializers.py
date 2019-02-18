"""Mission Control serializers."""
from django.db.utils import IntegrityError
from rest_framework import serializers
from oauth2_provider.models import Application

from .models import Rover, BlockDiagram


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


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'
        read_only_fields = ('user',)
