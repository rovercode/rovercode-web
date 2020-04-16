# -*- coding: utf-8 -*-
"""API urls."""
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from . import views

router = routers.DefaultRouter()
router.register(r'block-diagrams', views.BlockDiagramViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token, name='api-token-auth'),
    url(r'^api-token-verify/', verify_jwt_token, name='api-token-verify'),
    url(r'^v1/', include((router.urls, 'api'), namespace='v1')),
    url(r'^$', RedirectView.as_view(
        pattern_name='api:v1:api-root', permanent=False)),
]
