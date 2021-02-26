"""Authorize urls."""
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from dj_rest_auth.registration.views import SocialAccountDisconnectView
from dj_rest_auth.registration.views import SocialAccountListView

from authorize import views


OAUTH_CALLBACK = r'^auth/social/{provider}/callback'

github_urlpatterns = [
    url(
        r'^auth-server/',
        csrf_exempt(views.JsonAdapterView.adapter_view(views.GitHubAdapter)),
        name='github_auth_server'
    ),
    url(
        r'^login/',
        views.GitHubLogin.as_view(),
        name='github_callback_login',
    ),
]
google_urlpatterns = [
    url(
        r'^auth-server/',
        csrf_exempt(views.JsonAdapterView.adapter_view(views.GoogleAdapter)),
        name='google_auth_server'
    ),
    url(
        r'^login/',
        views.GoogleLogin.as_view(),
        name='google_callback_login',
    ),
]

urlpatterns = [
    url(r'^auth/', include('dj_rest_auth.urls')),
    url(r'^auth/registration/', include('dj_rest_auth.registration.urls')),
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
]
