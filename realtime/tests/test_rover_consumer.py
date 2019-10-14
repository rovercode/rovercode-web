"""Rover websocket consumer test."""
import json
import pytest
from django.conf.urls import url
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from realtime.consumers import RoverConsumer
from middleware.tests.mock_auth_middleware \
    import MockAuthMiddleware, MOCK_USER_ID
from mission_control.models import Rover
from oauth2_provider.models import Application
from rovercode_web.users.models import User


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_rover_consumer():
    """Test sending a message to the room and having it echo it back."""
    user = User.objects.create(id=MOCK_USER_ID)
    oauth_app = Application.objects.create(
        user=user,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        client_type=Application.CLIENT_CONFIDENTIAL,
        name='rover'
    )
    Rover.objects.create(
        name='rover',
        owner=user,
        local_ip='8.8.8.8',
        oauth_application=oauth_app
    )
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ]))
    communicator = WebsocketCommunicator(
        application,
        "/ws/realtime/{}/".format(oauth_app.client_id)
    )
    connected, _ = await communicator.connect()
    assert connected
    message = json.dumps({"message": "hello"})
    # Test sending text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    assert response == message
    # Close
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_rover_consumer_shared_user():
    """Test sending a message to the room as a shared user."""
    creating_user = User.objects.create(id=MOCK_USER_ID + 100,
                                        username="creator")
    shared_user = User.objects.create(id=MOCK_USER_ID,
                                      username="creator's buddy")
    oauth_app = Application.objects.create(
        user=creating_user,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        client_type=Application.CLIENT_CONFIDENTIAL,
        name='rover'
    )
    rover = Rover.objects.create(
        name='rover',
        owner=creating_user,
        local_ip='8.8.8.8',
        oauth_application=oauth_app,
    )
    rover.shared_users.add(shared_user)
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ]))
    communicator = WebsocketCommunicator(
        application,
        "/ws/realtime/{}/".format(oauth_app.client_id)
    )
    connected, _ = await communicator.connect()
    assert connected
    message = json.dumps({"message": "hello"})
    # Test sending text
    await communicator.send_to(text_data=message)
    response = await communicator.receive_from()
    assert response == message
    # Close
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_rover_consumer_no_user():
    """Test trying to connect while unauthenticated."""
    User.objects.create(id=MOCK_USER_ID)
    application = URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ])
    communicator = WebsocketCommunicator(application,
                                         "/ws/realtime/{}/".format('foobar'))
    connected, code = await communicator.connect()
    assert code == 401
    assert not connected


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_rover_consumer_nonexistent_client_id():
    """Test trying to connect to a nonexistent rover."""
    user = User.objects.create(id=MOCK_USER_ID + 1)
    oauth_app = Application.objects.create(
        user=user,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        client_type=Application.CLIENT_CONFIDENTIAL,
        name='rover'
    )
    Rover.objects.create(
        name='rover',
        owner=user,
        local_ip='8.8.8.8',
        oauth_application=oauth_app
    )
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ]))
    communicator = WebsocketCommunicator(
        application,
        "/ws/realtime/{}/".format("not_a_real_clientid")
    )
    connected, code = await communicator.connect()
    assert code == 404
    assert not connected


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_rover_consumer_disallowed_user():
    """Test trying to connect to a rover the user doesn't own."""
    user = User.objects.create(id=MOCK_USER_ID + 1)
    oauth_app = Application.objects.create(
        user=user,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        client_type=Application.CLIENT_CONFIDENTIAL,
        name='rover'
    )
    Rover.objects.create(
        name='rover',
        owner=user,
        local_ip='8.8.8.8',
        oauth_application=oauth_app
    )
    application = MockAuthMiddleware(URLRouter([
        url(r'^ws/realtime/(?P<room_name>[^/]+)/$', RoverConsumer),
    ]))
    communicator = WebsocketCommunicator(
        application,
        "/ws/realtime/{}/".format(oauth_app.client_id)
    )
    connected, code = await communicator.connect()
    assert code == 403
    assert not connected
