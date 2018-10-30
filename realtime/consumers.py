"""Consumers for Realtime app."""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from mission_control.models import Rover


class RoverConsumer(WebsocketConsumer):
    """Handles bidir communication between rover and browser clients."""

    room_name = None
    room_group_name = None

    def connect(self):
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            rover = Rover.objects.get(oauth_application__client_id=self.room_name)
        except Rover.DoesNotExist:
            self.close()
            return

        if rover.owner.id != user.id:
            self.close()
            return

        print("Realtime: user {} connected to rover {}".format(user, self.room_name))

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, _):
        """Handle disconnections."""
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """Handle messages received via WebSocket connection."""
        text_data_json = json.loads(text_data)
        message_raw = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'group_message',
                'message': message_raw
            }
        )

    def group_message(self, event):
        """Handle messages received via the room group channel layer."""
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
