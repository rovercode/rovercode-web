"""Rover websocket consumer test"""
import pytest
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
    # # Test sending text
    # await communicator.send_to(text_data="hello")
    # response = await communicator.receive_from()
    # assert response == "hello"
    # # Close
    await communicator.disconnect()
