# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from events.forms import EventCreateForm, EventImageForm
from events.models import Event, EventImage


class EventCreateView(CreateView):
    form_class = EventCreateForm
    template_name = 'base/form.html'
    success_url = '/events'

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'New Event'
        context['title'] = 'Events'
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

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(EventDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(EventDeleteView, self).post(request, *args, **kwargs)

class EventImageCreateView(CreateView):
    form_class = EventImageForm
    template_name = 'base/form.html'

    def get_context_data(self, **kwargs):
        context = super(EventImageCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'New image'
        context['title'] = 'Images'
        return context

class EventImageUpdateView(UpdateView):
    form_class = EventImageForm
    template_name = 'base/form.html'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().event.user):
            redirect('permission_denied')
        return super(EventImageUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventImageUpdateView, self).get_context_data(**kwargs)
        context['heading'] = 'Update Image'
        context['title'] = 'Images'
        return context

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().event.user):
            redirect('permission_denied')
        return super(EventImageUpdateView, self).post(request, *args, **kwargs)


class EventImageDeleteView(DeleteView):
    model = EventImage
    template_name = 'events/confirm_delete.html'
    success_url = reverse_lazy('events')


class EventListView(ListView):
    model = Event

class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        else:
            context['edit_permission'] = False
        return context