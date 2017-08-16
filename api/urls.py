# -*- coding: utf-8 -*-
"""API urls."""
from __future__ import unicode_literals

from django.conf.urls import include, url
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'rovers', views.RoverViewSet, base_name='rover')
router.register(r'block-diagrams', views.BlockDiagramViewSet)


urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
]
