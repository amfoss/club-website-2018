# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from registration.forms import UserSignUpForm
from registration.models import UserInfo


class UserSignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signup_success')

    def get_context_data(self, **kwargs):
        context = super(UserSignUpView, self).get_context_data(**kwargs)
        context['signup'] = True
        return context


class UserSignUpSuccess(TemplateView):
    template_name = 'registration/signup_success.html'

class ProfileView(ListView):
    template_name = 'profile/profile.html'
    model = UserInfo


def login(request,  *args, **kwargs):  # view to handle remember me
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)
