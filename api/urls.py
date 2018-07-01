# -*- coding: utf-8 -*-
"""API urls."""
from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import verify_jwt_token

from . import views

router = routers.DefaultRouter()
router.register(r'rovers', views.RoverViewSet, base_name='rover')
router.register(r'block-diagrams', views.BlockDiagramViewSet)


urlpatterns = [
    url(r'^$', get_swagger_view(title='rovercode API')),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^v1/', include(router.urls, namespace='v1')),
]
