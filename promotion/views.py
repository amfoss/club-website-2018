# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from smtplib import SMTPException

from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.mail import send_mail


from promotion.forms import JoinApplicationForm
from promotion.models import JoinApplication


approve_mail_content = ',\\n\\nWe are exited to inform that you are selected for the interview.'
reject_mail_content = ',\\n\\nWe are sorry to inform that you are not selected for the interview. Please try again ' \
                      'next time.'


class JoinApplicationListView(ListView):
    model = JoinApplication
    queryset = JoinApplication.objects.filter(is_approved=False, is_rejected=False)

    def get_context_data(self, **kwargs):
        context = super(JoinApplicationListView, self).get_context_data(**kwargs)
        context['count'] = len(context['object_list'])
        return context


class JoinApplicationDetailView(DetailView):
    model = JoinApplication

    def get_context_data(self, **kwargs):
        context = super(JoinApplicationDetailView, self).get_context_data(**kwargs)
        context['approve_mail_subject'] = 'Congrats! FOSS@Amrita membership application'
        context['approve_mail_content'] = 'Hi ' + self.get_object().name + approve_mail_content
        context['reject_mail_subject'] = 'FOSS@Amrita membership application'
        context['reject_mail_content'] = 'Hi ' + self.get_object().name + reject_mail_content
        context['mail_error'] = kwargs.get('mail_errors', None)
        return context


class JoinApplicationCreateView(CreateView):
    form_class = JoinApplicationForm
    template_name = 'base/form.html'


class EmailForm(forms.Form):
    mail_id = forms.EmailField()
    mail_subject = forms.CharField()
    mail_content = forms.CharField()


class JoinApplicationUpdateView(UpdateView):
    model = JoinApplication
    fields = ['is_approved']

    def get(self, **kwargs):
        return HttpResponse('This view accepts only post requests')

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            return redirect('permission_denied')

        form = EmailForm(request.POST)

        if form.is_valid():
            # mail id of all the admins and the mail id from the form
            to_address_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
            to_address_list.append(form.cleaned_data['mail_id'])

            # sent mail, if there are errors in mail, check that too
            mail_errors = False
            try:
                send_mail(form.cleaned_data['mail_subject'], form.cleaned_data['mail_content'],
                          'amritapurifoss@gmail.com', to_address_list, fail_silently=False)
            except SMTPException:
                mail_errors = True

            # render the detail page
            return redirect('join_detail', self.get_object().id)

        # error in form
        return redirect('join_detail', self.get_object().id)
