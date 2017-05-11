# -*- coding: utf-8 -*-
"""Mission Control urls."""
from __future__ import unicode_literals

from django.conf.urls import include, url
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'rovers', views.RoverViewSet)
router.register(r'block-diagrams', views.BlockDiagramViewSet)


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^load/(?P<bd>[0-9]+)/$', views.home, name='home_with_load'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^list/$', views.list, name='list'),
]
