# -*- coding: utf-8 -*-
"""Users adapters."""
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    """Account adapter."""

    def is_open_for_signup(self, request):
        """Return if signup is allowed."""
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Social account adapter."""

    def is_open_for_signup(self, request, sociallogin):
        """Return if signup is allowed."""
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
