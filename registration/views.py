# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView


class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'username', 'password']
    template_name = 'registration/signup.html'
