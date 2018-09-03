# realtime/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/realtime/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
