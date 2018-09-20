"""Rover websocket consumer test"""

from channels.testing import WebsocketCommunicator
communicator = WebsocketCommunicator(SimpleWebsocketApp, "/testws/")
connected, subprotocol = await communicator.connect()
assert connected
# Test sending text
await communicator.send_to(text_data="hello")
response = await communicator.receive_from()
assert response == "hello"
# Close
await communicator.disconnect()
