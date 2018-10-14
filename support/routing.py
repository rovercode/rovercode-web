"""Routing for the Support app."""
from django.conf.urls import url  # pragma: no cover

from . import consumers  # pragma: no cover


websocket_urlpatterns = [  # pragma: no cover
    url(r'^ws/support/(?P<room_name>[^/]+)/$',
        consumers.SupportConsumer),  # pragma: no cover
]
