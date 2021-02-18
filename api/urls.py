# -*- coding: utf-8 -*-
"""API urls."""
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from rovercode_web.users.utils import JwtObtainPairSerializer
from rovercode_web.users.utils import JwtRefreshSerializer

from . import views

router = routers.DefaultRouter()
router.register(
    r'block-diagrams', views.BlockDiagramViewSet, basename='blockdiagram')
router.register(r'courses', views.CourseViewSet)
router.register(r'lessons', views.LessonViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(
        r'^api-token-auth/',
        TokenObtainPairView.as_view(serializer_class=JwtObtainPairSerializer),
        name='api-token-auth'
    ),
    url(
        r'^api-token-verify/',
        TokenVerifyView.as_view(),
        name='api-token-verify'
    ),
    url(
        r'^api-token-refresh/',
        TokenRefreshView.as_view(serializer_class=JwtRefreshSerializer),
        name='api-token-refresh'
    ),
    url(r'^v1/', include((router.urls, 'api'), namespace='v1')),
    url(r'^$', RedirectView.as_view(
        pattern_name='api:v1:api-root', permanent=False)),
]
