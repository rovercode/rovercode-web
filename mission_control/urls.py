# -*- coding: utf-8 -*-
"""Mission Control urls."""
from __future__ import unicode_literals

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^load/(?P<bd>[0-9]+)/$', views.home, name='home_with_load'),
    url(r'^bd-list/$', views.bd_list, name='bd_list'),
]
