# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, UpdateView

from noticeBoard.models import Notice


class NoticeCreateView(CreateView):
    template_name = 'base/form.html'
    model = Notice

    def get_context_data(self, **kwargs):
        context = super(NoticeCreateView, self).get_context_data(**kwargs)
        context['heading'] = "Post a notice"
        return context

    def form_valid(self, form):
        form = super(NoticeCreateView, self).form_valid(form)
        user = self.request.user
        self.object.user = user
        self.object.save()
        return form


