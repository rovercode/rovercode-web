"""Authorize views."""
from django.conf import settings
from django.utils.translation import gettext as _

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthAction
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import CallbackSerializer


class BaseLogin(APIView):
    """Base login view."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Return the URL of provider's authentication server."""
        adapter = self.adapter_class(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)
        view = OAuth2LoginView()
        view.request = request
        view.adapter = adapter
        client = view.get_client(request, app)
        action = AuthAction.AUTHENTICATE
        auth_params = provider.get_auth_params(request, action)
        client.state = SocialLogin.stash_state(request)
        url = client.get_redirect_url(adapter.authorize_url, auth_params)
        return Response({'url': url})


class BaseCallbackConnect(SocialConnectView):
    """Base callback connect."""

    def get_response(self):
        """Get the connection response."""
        return Response({'detail': _('Connection completed.')})


class GitHubCallbackMixin:
    """Callback setup for Github."""

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CallbackSerializer

    @property
    def callback_url(self):
        """Github callback URL."""
        return settings.SOCIAL_CALLBACK_URL.format(service='github')


class GitHubCallbackCreate(GitHubCallbackMixin, SocialLoginView):
    """Log the user in. Creates a new user account if it doesn't exist yet."""


class GitHubCallbackConnect(GitHubCallbackMixin, BaseCallbackConnect):
    """Connect a provider's user account to the currently logged in user."""


class GitHubLogin(BaseLogin):
    """Login setup for Github."""

    adapter_class = GitHubOAuth2Adapter


class GoogleCallbackMixin:
    """Callback setup for Google."""

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CallbackSerializer

    @property
    def callback_url(self):
        """Google callback URL."""
        return settings.SOCIAL_CALLBACK_URL.format(service='google')


class GoogleCallbackCreate(GoogleCallbackMixin, SocialLoginView):
    """Log the user in. Creates a new user account if it doesn't exist yet."""


class GoogleCallbackConnect(GoogleCallbackMixin, BaseCallbackConnect):
    """Connect a provider's user account to the currently logged in user."""


class GoogleLogin(BaseLogin):
    """Login setup for Github."""

    adapter_class = GoogleOAuth2Adapter
