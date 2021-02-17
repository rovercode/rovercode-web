"""Authorize views."""
from django.conf import settings
from django.http import JsonResponse

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from dj_rest_auth.registration.views import SocialLoginView

from .serializers import CallbackSerializer


class JsonAdapterView(OAuth2LoginView):
    """View that returns the authorization URL for the service."""

    def dispatch(self, request, *args, **kwargs):
        """Return the url."""
        response = super().dispatch(request, *args, **kwargs)
        return JsonResponse({
            'url': response.url,
        })


class SocialLoginViewWithNextParam(SocialLoginView):
    """Add the 'next' parameter to the response."""

    def post(self, request, *args, **kwargs):
        """Process login. Provide the `next` parameter if it exists."""
        state, _ = self.request.session.get(
            'socialaccount_state', (None, None))

        response = super().post(request, *args, **kwargs)
        response.data['next_url'] = state.get('next') if state else None

        return response


class GitHubAdapter(GitHubOAuth2Adapter):
    """Customize the callback url to point to the frontend route."""

    @staticmethod
    def get_callback_url(request, app):
        """Return the frontend github callback route."""
        del request, app
        return settings.SOCIAL_CALLBACK_URL.format(service='github')


class GitHubLogin(SocialLoginViewWithNextParam):
    """Log the user in. Creates a new user account if it doesn't exist yet."""

    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CallbackSerializer
    callback_url = settings.SOCIAL_CALLBACK_URL.format(service='github')


class GoogleAdapter(GoogleOAuth2Adapter):
    """Customize the callback url to point to the frontend route."""

    @staticmethod
    def get_callback_url(request, app):
        """Return the frontend google callback route."""
        del request, app
        return settings.SOCIAL_CALLBACK_URL.format(service='google')


class GoogleLogin(SocialLoginViewWithNextParam):
    """Log the user in. Creates a new user account if it doesn't exist yet."""

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = CallbackSerializer
    callback_url = settings.SOCIAL_CALLBACK_URL.format(service='google')
