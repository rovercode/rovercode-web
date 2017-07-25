"""Mission Control serializers."""
from .models import Rover, BlockDiagram
from rest_framework import serializers


class RoverSerializer(serializers.ModelSerializer):
    """Rover model serializer."""

    class Meta:
        """Meta class."""

        model = Rover
        fields = (
            'id', 'name', 'owner', 'local_ip', 'last_checkin',
            'left_forward_pin', 'left_backward_pin', 'right_forward_pin',
            'right_backward_pin', 'left_eye_pin', 'right_eye_pin',
        )
        read_only_fields = ('owner',)


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'
        read_only_fields = ('user',)
