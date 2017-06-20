# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from promotion.models import JoinApplication


class JoinApplicationListView(ListView):
    model = JoinApplication


class JoinApplicationDetailView(DetailView):
    model = JoinApplication


class JoinApplicationCreateView(CreateView):
    model = JoinApplication
    template_name = 'base/form.html'
