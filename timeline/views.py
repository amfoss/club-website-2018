# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from timeline.models import AlumniInfo


class AlumniListView(ListView):
    model = AlumniInfo
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super(AlumniListView, self).get_context_data(**kwargs)
        context['objects'] = AlumniInfo.objects.order_by('-date')
        return context
