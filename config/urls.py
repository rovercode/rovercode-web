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
    url(r'^users/', include('rovercode_web.users.urls', namespace='users')),
    url(r'^authorize/', include('allauth.urls')),

    url(r'^realtime/', include('realtime.urls', namespace='realtime')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^jwt/', include('authorize.urls', namespace='jwt')),
    url(r'^jwt/auth/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^docs/', include_docs_urls(
        title='Rovercode API',
        description='API for the rovercode web service.')),
    url(r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
