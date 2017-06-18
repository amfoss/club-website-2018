# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import *


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ['user', 'title', 'description', 'magazine', 'publication_date']

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article

    def get(self, request, *args, **kwargs):

        return super(ArticleUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):

        return super(ArticleUpdateView, self).post(request, *args, **kwargs)


class ArticleDeleteView(DeleteView):
    model = Article

    def get(self, request, *args, **kwargs):

        return super(ArticleDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        return super(ArticleDeleteView, self).post(request, *args, **kwargs)