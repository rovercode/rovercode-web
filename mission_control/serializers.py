"""Mission Control serializers."""
from .models import Rover, BlockDiagram
from rest_framework import serializers


class RoverSerializer(serializers.HyperlinkedModelSerializer):
    """Rover model serializer."""

    class Meta:
        """Meta class."""

        model = Rover
        fields = ('id', 'name', 'owner', 'local_ip', 'last_checkin')


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'
        read_only_fields = ('user',)
