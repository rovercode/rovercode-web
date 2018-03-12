# -*- coding: utf-8 -*-
"""Blog urls."""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, base_name='post')

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post-drafts-list/$',
        views.post_list, {'drafts': True},
        name='post_drafts_list'),
    url(r'^', include(router.urls)),
    url(r'^post-edit/(?P<slug>[-\w]+)/$',
        views.post_edit, name='post_edit'),
    url(r'^post-edit/$',
        views.post_edit, name='post_new'),
    url(r'^post-detail/(?P<slug>[-\w]+)/$',
        views.post_detail, name='post_detail'),
]
