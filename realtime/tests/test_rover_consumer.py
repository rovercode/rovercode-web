"""Rover websocket consumer test"""
from channels.testing import WebsocketCommunicator
from realtime.consumers import ChatConsumer

communicator = WebsocketCommunicator(ChatConsumer, "/testws/")
connected, subprotocol = await communicator.connect()
assert connected
# Test sending text
await communicator.send_to(text_data="hello")
response = await communicator.receive_from()
assert response == "hello"
# Close
await communicator.disconnect()
