"""Rover websocket consumer test."""
import json
import pytest
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from unittest.mock import MagicMock, patch
from realtime.consumers import RoverConsumer
from middleware.tests.mock_auth_middleware import MockAuthMiddleware, MOCK_USER_ID
from mission_control.models import Rover
from rovercode_web.users.models import User


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_rover_consumer():
    """Test sending a message to the room and having it echo it back."""
    user = User.objects.create(id=0)
    rover = Rover.objects.create(
        name='rover',
        owner=user,
        local_ip='8.8.8.8'
    )
    print(Rover.objects.all())
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ]))
    communicator = WebsocketCommunicator(application, "/ws/realtime/foobar/")
    connected, _ = await communicator.connect()
    assert connected
    message = json.dumps({"message": "hello"})
    # Test sending text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    assert response == message
    # Close
    await communicator.disconnect()
