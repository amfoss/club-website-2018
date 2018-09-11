from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class CustomLogin(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        return False

    def is_open_for_signup(self, request, sociallogin):
        return True

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            existing_user = User.objects.get(email=sociallogin.account.extra_data['email'])
            if existing_user.is_active:
                sociallogin.connect(request, existing_user)
            else:
                return
        except ObjectDoesNotExist:
            pass
