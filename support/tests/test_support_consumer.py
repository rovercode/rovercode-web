"""Support websocket consumer test."""
import json
import pytest
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from support.consumers import SupportConsumer
from support.models import SupportRequest
from rovercode_web.users.models import User
from mission_control.models import BlockDiagram
from middleware.tests.mock_auth_middleware \
    import MockAuthMiddleware, MOCK_USER_ID

@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_support_consumer():
    """Test sending a message to the room and having it echo it back."""
    user = User.objects.create(
        id=MOCK_USER_ID,
        username='me',
    )
    program = BlockDiagram.objects.create(
        user=user,
        name='test',
        content='<xml></xml>'
    )
    SupportRequest.objects.create(
        id=42,
        subject='Test Subject',
        body='Test body',
        experience_level=0,
        owner=user,
        program=program,
    )
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/support/(?P<room_name>[^/]+)/$', SupportConsumer),
    ]))
    communicator = WebsocketCommunicator(application, "/ws/support/42/")
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


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_support_consumer_blocked_user():
    """Test sending a message to the room and having it echo it back."""
    blocked_user = User.objects.create(id=MOCK_USER_ID, username='meanie')
    user = User.objects.create(
        id=100,
        username='me',
    )
    user.blocked_users.set([blocked_user])
    program = BlockDiagram.objects.create(
            user=user,
            name='test',
            content='<xml></xml>'
    )
    SupportRequest.objects.create(
        id=42,
        subject='Test Subject',
        body='Test body',
        experience_level=0,
        owner=user,
        program=program,
    )
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/support/(?P<room_name>[^/]+)/$', SupportConsumer),
    ]))
    communicator = WebsocketCommunicator(application, "/ws/support/42/")
    connected, _ = await communicator.connect()
    assert not connected
