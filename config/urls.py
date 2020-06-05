# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    # User management
    url(r'^authorize/', include('allauth.urls')),

    url(r'^api/', include(('api.urls', 'api'), namespace='api')),
    url(r'^api-auth/',
        include(('rest_framework.urls', 'restframework'), namespace='rest_framework')),
    url(r'^jwt/', include(('authorize.urls', 'authorize'), namespace='jwt')),
    url(r'^jwt/auth/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^docs/', include_docs_urls(
        title='Rovercode API',
        description='API for the rovercode web service.')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
