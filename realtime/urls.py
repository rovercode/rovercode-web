"""Urls for the Realtime app."""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='debug-index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='debug-room'),
]
