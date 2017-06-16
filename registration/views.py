# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView


from registration.forms import UserSignUpForm
from registration.models import UserInfo


class UserSignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signup_success')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('already_logged_in')
        return super(UserSignUpView, self).get(request, *args, **kwargs)

class ProfileView(DetailView):
  model = UserInfo




def login(request,  *args, **kwargs):  # view to handle remember me
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('already_logged_in')
    return auth_views.login(request, *args, **kwargs)
