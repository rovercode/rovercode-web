"""Routing for the Realtime app."""
from django.conf.urls import url  # pragma: no cover

from . import consumers  # pragma: no cover


websocket_urlpatterns = [  # pragma: no cover
    url(r'^ws/realtime/(?P<room_name>[^/]+)/$',
        consumers.RoverConsumer),  # pragma: no cover
]
