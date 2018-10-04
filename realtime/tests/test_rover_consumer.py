"""Rover websocket consumer test"""
import pytest
import json
from django.test import override_settings
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from realtime.consumers import ChatConsumer

@pytest.mark.asyncio
async def test_rover_consumer():
    application = URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', ChatConsumer),
    ])
    communicator = WebsocketCommunicator(application, "/ws/realtime/foobar/")
    connected, subprotocol = await communicator.connect()
    assert connected
    message = json.dumps({"message": "hello"})
    # Test sending text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    assert response == message
    # Close
    await communicator.disconnect()
