"""Rover websocket consumer test."""
import json
import pytest
from test_plus.test import TestCase
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from unittest.mock import MagicMock, patch
from realtime.consumers import RoverConsumer
from middleware.tests.mock_auth_middleware import MockAuthMiddleware, MOCK_USER_ID
from mission_control.models import Rover
from rovercode_web.users.models import User


@pytest.mark.asyncio
@patch("realtime.consumers.Rover")
async def test_rover_consumer(mock_rover):
    """Test sending a message to the room and having it echo it back."""
    mock_rover.objects.get.return_value = Rover(owner=User(id=MOCK_USER_ID))
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
