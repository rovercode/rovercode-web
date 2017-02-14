from .models import Rover, BlockDiagram
from rest_framework import serializers

class RoverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rover
        fields = ('name', 'owner', 'local_ip', 'last_checkin')


class BlockDiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockDiagram
        fields = ('id', 'user', 'name', 'content')
