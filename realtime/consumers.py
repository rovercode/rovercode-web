"""Consumers for Realtime app."""
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class RoverConsumer(WebsocketConsumer):
    """Handles bidir communication between rover and browser clients."""

    room_name = None
    room_group_name = None

    def connect(self):
        """Handle connections."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

        text_data_dict = json.loads(text_data)
        text_data_dict['type'] = 'group_message'

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_dict
        )

    def group_message(self, event):
        """Handle messages received via the room group channel layer."""

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
