"""Mission Control serializers."""
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
            'left_forward_pin', 'left_backward_pin', 'right_forward_pin',
            'right_backward_pin', 'left_eye_pin', 'right_eye_pin',
            'left_eye_i2c_port', 'left_eye_i2c_addr', 'right_eye_i2c_port',
            'right_eye_i2c_addr', 'client_id', 'client_secret'
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
        return Rover.objects.create(oauth_application=oauth_application,
                                    **validated_data)


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'
        read_only_fields = ('user',)
