# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from noticeBoard.forms import NoticeCreateForm
from noticeBoard.models import Notice


class NoticeCreateView(CreateView):
    form_class = NoticeCreateForm
    template_name = 'base/form.html'
    model = Notice

    def get_context_data(self, **kwargs):
        context = super(NoticeCreateView, self).get_context_data(**kwargs)
        context['heading'] = "Post a message"
        return context

    def form_valid(self, form):
        form = super(NoticeCreateView, self).form_valid(form)
        user = self.request.user
        self.object.user = user
        self.object.save()
        return form


class NoticeUpdateView(UpdateView):
    form_class = NoticeCreateForm
    template_name = 'base/form.html'
    model = Notice

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(NoticeUpdateView, self).get(request, *args, **kwargs)


class NoticeDeleteView(DeleteView):
    model = Notice
    success_url = reverse_lazy('notices')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(NoticeDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(NoticeDeleteView, self).post(request, *args, **kwargs)


class NoticeListView(ListView):
    model = Notice

    def get_context_data(self, **kwargs):
        context = super(NoticeListView, self).get_context_data()
        if self.request.user.is_superuser or self.request.user == self.object.user:
            context['edit_permission'] = True
        else:
            context['edit_permission'] = False
        print(context['edit_permission'])
        return context
