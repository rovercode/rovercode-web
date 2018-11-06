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
router.register(r'rovers', views.RoverViewSet, base_name='rover')
router.register(r'block-diagrams', views.BlockDiagramViewSet)
router.register(r'support-requests', views.SupportRequestViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^v1/', include(router.urls, namespace='v1')),
    url(r'^$', RedirectView.as_view(
        pattern_name='api:v1:api-root', permanent=False)),
]
