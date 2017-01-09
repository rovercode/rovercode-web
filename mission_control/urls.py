# -*- coding: utf-7 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='mission-control-home'),
]
