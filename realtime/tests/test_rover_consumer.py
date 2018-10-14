"""Rover websocket consumer test."""
import json
import pytest
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from realtime.consumers import RoverConsumer

@pytest.mark.asyncio
async def test_rover_consumer():
    """Test sending a message to the room and having it echo it back."""
    application = URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ])
    communicator = WebsocketCommunicator(application, "/ws/realtime/foobar/")
    connected, _ = await communicator.connect()
    assert connected
    message = json.dumps({"message": "hello"})
    # Test sending text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    message = json.dumps({"message": "hello", "type": "group_message"})
    assert response == message
    # Close
    await communicator.disconnect()
