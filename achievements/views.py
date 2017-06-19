# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'area', 'description', 'magazine', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'area', 'description', 'magazine', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ArticleUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ArticleUpdateView, self).post(request, *args, **kwargs)


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('article')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ArticleDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ArticleDeleteView, self).post(request, *args, **kwargs)


# Contribution views


class ContributionListView(ListView):
    model = Contribution


class ContributionDetailView(DetailView):
    model = Contribution

    def get_context_data(self, **kwargs):
        context = super(ContributionDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context


class ContributionCreateView(CreateView):
    model = Contribution
    fields = ['contribution_id', 'title', 'organisation', 'url', 'description', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContributionCreateView, self).form_valid(form)


class ContributionUpdateView(UpdateView):
    model = Contribution
    fields = ['contribution_id', 'title', 'organisation', 'url', 'description', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContributionUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionUpdateView, self).post(request, *args, **kwargs)


class ContributionDeleteView(DeleteView):
    model = Contribution
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('contribution')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionDeleteView, self).post(request, *args, **kwargs)


# GSoc Views

# Speaker views


class SpeakerListView(ListView):
    model = Speaker


class SpeakerDetailView(DetailView):
    model = Speaker

    def get_context_data(self, **kwargs):
        context = super(SpeakerDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context


class SpeakerCreateView(CreateView):
    model = Speaker
    fields = ['title', 'type', 'conference_name', 'location', 'url', 'date', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SpeakerCreateView, self).form_valid(form)


class SpeakerUpdateView(UpdateView):
    model = Speaker
    fields = ['title', 'type', 'conference_name', 'location', 'url', 'date', 'description']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SpeakerUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerUpdateView, self).post(request, *args, **kwargs)


class SpeakerDeleteView(DeleteView):
    model = Speaker
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('speaker')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerDeleteView, self).post(request, *args, **kwargs)
