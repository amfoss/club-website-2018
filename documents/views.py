# created by Navaneeth S, navisk13@gmail.com

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from documents.models import Document
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
# Create your views here.


class DocumentListView(ListView):
    model = Document


class DocumentCreateView(CreateView):
    model = Document
    fields = ['title', 'document']
    success_url = '/documents'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(DocumentCreateView, self).form_valid(form)
        return response


class DocumentDeleteView(DeleteView):
    model = Document
    success_url = reverse_lazy('document')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(DocumentDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(DocumentDeleteView, self).post(request, *args, **kwargs)



