"""Authorize urls."""
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_auth.registration.views import (
    SocialAccountListView, SocialAccountDisconnectView
)

from authorize import views


OAUTH_CALLBACK = r'^auth/social/{provider}/callback'

github_urlpatterns = [
    url(
        r'^auth-server/',
        views.GitHubLogin.as_view(),
        name='github_auth_server'
    ),
    url(
        r'^login/',
        views.GitHubCallbackCreate.as_view(),
        name='github_callback_login',
    ),
    url(
        r'^connect/',
        views.GitHubCallbackConnect.as_view(),
        name='github_callback_connect',
    ),
]
google_urlpatterns = [
    url(
        r'^auth-server/',
        views.GoogleLogin.as_view(),
        name='google_auth_server'
    ),
    url(
        r'^login/',
        views.GoogleCallbackCreate.as_view(),
        name='google_callback_login',
    ),
    url(
        r'^connect/',
        views.GoogleCallbackConnect.as_view(),
        name='google_callback_connect',
    ),
]

urlpatterns = [
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/social/github/', include(github_urlpatterns)),
    url(r'^auth/social/google/', include(google_urlpatterns)),
    url(
        r'^auth/user/accounts/',
        SocialAccountListView.as_view(),
        name='social_account_list',
    ),
    url(
        r'^auth/user/accounts/<int:pk>/disconnect/',
        SocialAccountDisconnectView.as_view(),
        name='social_account_disconnect',
    ),
    url(
        OAUTH_CALLBACK.format(provider='github'),
        TemplateView.as_view(),
        name='github_callback',
    ),
    url(
        OAUTH_CALLBACK.format(provider='google'),
        TemplateView.as_view(),
        name='google_callback',
    ),
]
