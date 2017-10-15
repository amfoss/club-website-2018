# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import CreateView, UpdateView

from events.forms import EventCreateForm
from events.models import Event


class EventCreateView(CreateView):
    form_class = EventCreateForm
    template_name = 'base/form.html'
    success_url = '/events'

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'New Workshop'
        context['title'] = 'Workshops'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreateView, self).form_valid(form)

class EventUpdateView(UpdateView):
    form_class = EventCreateForm
    template_name = 'base/form.html'
    model = Event

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(EventUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['heading'] = 'Update Event'
        context['title'] = 'Events'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(EventUpdateView, self).post(request, *args, **kwargs)
