# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.forms.utils import ErrorList
from django.urls import reverse
from django.views.generic import DetailView, CreateView
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from fosswebsite.settings import join_application_mail_list, join_application_reply_to
from workshop.forms import WorkshopRegistrationForm
from workshop.models import Workshop, WorkshopRegistration


class WorkshopDetailView(DetailView):
    model = Workshop
    pk_url_kwarg = 'workshop_id'

    def get_context_data(self, **kwargs):
        context = super(WorkshopDetailView, self).get_context_data(**kwargs)
        registrations = WorkshopRegistration.objects.filter(workshop=self.get_object())
        print(len(registrations))
        no_of_seats_left = self.get_object().number_of_seats - len(registrations)
        context['seats_left'] = True
        if no_of_seats_left <= 0:
            context['seats_left'] = False
            no_of_seats_left = 0
        context['no_of_seats_left'] = no_of_seats_left
        return context


class WorkshopRegisterView(CreateView):
    form_class = WorkshopRegistrationForm
    template_name = 'base/form.html'
    success_url = '/workshop/success/'

    def get_context_data(self, **kwargs):
        context = super(WorkshopRegisterView, self).get_context_data(**kwargs)
        context['heading'] = Workshop.objects.get(id=self.kwargs.get('workshop_id', None)).name
        return context

    def form_valid(self, form):

        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))

        try:
            application = WorkshopRegistration.objects.filter(email=form.cleaned_data.get('email'))
        except WorkshopRegistration.DoesNotExist:
            application = None

        if application.exists():
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                u'Your are already registered'
            ])
            return self.form_invalid(form)

        valid_form = super(WorkshopRegisterView, self).form_valid(form)

        # generate urls
        list_url = ''.join(['http://', get_current_site(self.request).domain, reverse('join_list')])

        # mail data
        subject = 'Registration for ' + workshop.name + ' - ' + form.cleaned_data.get('name')
        content = form.cleaned_data.get('name') + ' registered for ' + workshop.name + ' at ' + \
                  str(datetime.datetime.now()) + '. \n\nPlease visit ' + list_url + ' for more details.'

        to_address_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))

        # sent mail when application is submitted
        send_mail(subject, content, 'amritapurifoss@gmail.com', to_address_list, fail_silently=False)

        mail_content = "Hi " + form.cleaned_data.get('name') + ", \n\n" + \
                       "Great to know that you are interested in '" + workshop.name + "' workshop conducted by" \
                       "FOSS@Amrita. We got your application and it's being processed. " + \
                       "We will get back to you once your payment process is is complete.\n\n" \
                       "Please pay Rs" + str(workshop.price) + " at FOSS club, ground floor lab after 4:30pm on or " + \
                       "before " + str(workshop.start_date_time.date()) + " or contact us at " + \
                       "8547801861, 7034890948, 703400210 during breaks. \n\nNote: Payment has to completed " + \
                       "before the last date. You should show the confirmation e-mail to attend the workshop." + \
                       " \n\nThank you, \n\nFOSS@Amrita"

        to_address_list = join_application_reply_to
        to_address_list.append(form.cleaned_data.get('email'))
        email = EmailMessage(
            workshop.name + ' registartion',
            mail_content,
            'amritapurifoss@gmail.com',
            to_address_list,
            join_application_mail_list,
            reply_to=join_application_reply_to,
            headers={'Message-ID': 'foss@amrita'},
        )
        email.send(fail_silently=False)
        to_address_list.remove(form.cleaned_data.get('email'))

        self.object.workshop = workshop
        self.object.save()

        return valid_form
