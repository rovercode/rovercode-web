"""Consumers for Support app."""
import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from middleware.tests.mock_auth_middleware \
    import MockAuthMiddleware, MOCK_USER_ID
from .models import SupportRequest
LOGGER = logging.getLogger(__name__)


class SupportConsumer(WebsocketConsumer):
    """Handles bidir communication between support clients."""

    room_name = None
    room_group_name = None

    def connect(self):
        """Handle connections."""
        user = self.scope.get('user')
        if not user or user.is_anonymous:
            self.close(code=401)
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            supportRequest = SupportRequest.objects.get(id=int(self.room_name))
        except (SupportRequest.DoesNotExist, ValueError):
            self.close(code=404)
            return

        blocked_user_ids = [user.id for user in supportRequest.owner.blocked_users.all()]
        if user.id in blocked_user_ids:
            self.close(code=404)
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        LOGGER.info("Support: user %s connected to rover %s",
                    user, self.room_name)

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
