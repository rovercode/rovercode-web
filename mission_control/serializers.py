from .models import Rover
from rest_framework import serializers

class RoverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rover
        fields = ('name', 'owner', 'local_ip', 'last_checkin')
