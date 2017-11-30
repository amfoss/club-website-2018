# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView

from timeline.models import AlumniInfo


class AlumniListView(ListView):
    model = AlumniInfo
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super(AlumniListView, self).get_context_data(**kwargs)
        context['objects'] = AlumniInfo.objects.order_by('-date')
        return context


class AlumniCreateView(CreateView):
    model = AlumniInfo
    fields = ['name', 'email', 'profile_pic', 'position', 'description', 'resume', 'date']
    success_url = '/timeline'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super(AlumniCreateView, self).form_valid(form)
        return response

