"""Consumers for Realtime app."""
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from mission_control.models import Rover
LOGGER = logging.getLogger(__name__)


class RoverConsumer(WebsocketConsumer):
    """Handles bidir communication between rover and browser clients."""

    room_name = None
    room_group_name = None

    def connect(self):
        """Handle new connection requests."""
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            self.close(code=401)
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            rover = Rover.objects.get(
                oauth_application__client_id=self.room_name)
        except Rover.DoesNotExist:
            self.close(code=404)
            return

        print("\n\n\n\n\nShared users:")
        print(rover.shared_users.all())
        print(user.id)
        print("\n\n\n\n")
        if user != rover.owner and user not in rover.shared_users.all():
            self.close(code=403)
            return

        LOGGER.info("Realtime: user %s connected to rover %s",
                    user, self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, _):
        """Handle disconnections."""
        # Leave room group
        if self.room_group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        """Handle messages received via WebSocket connection."""
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'group_message',
                'body': text_data
            }
        )

    def group_message(self, event):
        """Handle messages received via the room group channel layer."""
        # Send message to WebSocket
        self.send(text_data=event['body'])
