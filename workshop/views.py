# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.forms.utils import ErrorList
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from fosswebsite.settings import join_application_mail_list, join_application_reply_to
from workshop.forms import WorkshopRegistrationForm, FeedbackForm, WorkshopForm
from workshop.models import Workshop, WorkshopRegistration, WorkshopGallery, WorkshopFeedback


class WorkshopDetailView(DetailView):
    model = Workshop
    pk_url_kwarg = 'workshop_id'

    def get_context_data(self, **kwargs):
        context = super(WorkshopDetailView, self).get_context_data(**kwargs)
        registrations = WorkshopRegistration.objects.filter(workshop=self.get_object())
        if self.get_object().number_of_seats is not None:
            no_of_seats_left = self.get_object().number_of_seats - len(registrations)
            context['seats_left'] = True
            if no_of_seats_left <= 0:
                context['seats_left'] = False
                no_of_seats_left = 0
            context['no_of_seats_left'] = no_of_seats_left
        feedback = WorkshopFeedback.objects.filter(workshop=self.get_object())
        context['feedback'] = feedback
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        print(self.get_object().price)
        return context


class WorkshopCreateView(CreateView):
    form_class = WorkshopForm
    template_name = 'base/form.html'
    success_url = '/workshop'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(WorkshopCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkshopCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'New Workshop'
        context['title'] = 'Workshops'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(WorkshopCreateView, self).form_valid(form)


class WorkshopUpdateView(UpdateView):
    form_class = WorkshopForm
    template_name = 'base/form.html'
    model = Workshop

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(WorkshopUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkshopUpdateView, self).get_context_data(**kwargs)
        context['heading'] = 'Update Workshop'
        context['title'] = 'Workshops'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(WorkshopUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(WorkshopUpdateView, self).post(request, *args, **kwargs)


class WorkshopDeleteView(DeleteView):
    model = Workshop
    template_name = 'workshop/confirm_delete.html'
    success_url = reverse_lazy('workshop_list')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(WorkshopDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(WorkshopDeleteView, self).post(request, *args, **kwargs)


class WorkshopRegisterFormView(CreateView):
    form_class = WorkshopRegistrationForm
    template_name = 'base/form.html'
    success_url = '/workshop/success/'

    def get(self, request, *args, **kwargs):
        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))
        if len(WorkshopRegistration.objects.filter(workshop=workshop)) >= workshop.number_of_seats:
            return redirect(reverse('workshop_detail', kwargs={'workshop_id': kwargs.get('workshop_id', None)}))
        return super(WorkshopRegisterFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkshopRegisterFormView, self).get_context_data(**kwargs)
        context['heading'] = Workshop.objects.get(id=self.kwargs.get('workshop_id', None)).name
        return context

    def form_valid(self, form):

        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))

        try:
            application = WorkshopRegistration.objects.filter(workshop=workshop , email=form.cleaned_data.get('email'))
        except WorkshopRegistration.DoesNotExist:
            application = None

        if application.exists():
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                u'You are already registered'
            ])
            return self.form_invalid(form)

        valid_form = super(WorkshopRegisterFormView, self).form_valid(form)

        # generate urls
        # list_url = ''.join(['http://', get_current_site(self.request).domain,
        #                     reverse('workshop_list', kwargs={'workshop_id': workshop.id})])
        #
        # # mail data
        # subject = 'Registration for ' + workshop.name + ' - ' + form.cleaned_data.get('name')
        # content = form.cleaned_data.get('name') + ' registered for ' + workshop.name + ' at ' + \
        #           str(datetime.datetime.now()) + '. \n\nPlease visit ' + list_url + ' for more details.'
        #
        # to_address_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))

        # sent mail when application is submitted
        # send_mail(subject, content, 'amritapurifoss@gmail.com', to_address_list, fail_silently=False)

        mail_content = "Hi " + form.cleaned_data.get('name') + ", \n\n" + \
                       "Great to know that you are interested in '" + workshop.name + "' workshop conducted by" \
                                                                                      "FOSS@Amrita. We got your application and it's being processed. " + \
                       "We will get back to you once your payment process is is complete.\n\n" \
                       "Please pay Rs" + str(workshop.price) + " at FOSS club, ground floor lab after 4:30pm on or " + \
                       "before " + str(workshop.start_date_time.date()) + " or contact us at " + \
                       str(workshop.contact_info) + " during breaks. \n\nNote: Payment has to completed " + \
                       "before the last date. You should show the confirmation e-mail to attend the workshop." + \
                       " \n\nThank you, \n\nFOSS@Amrita"

        to_address_list = ['chirath.02@gmail.com', form.cleaned_data.get('email')]
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


class WorkshopRegistrationListView(ListView):
    model = WorkshopRegistration

    def get_context_data(self, **kwargs):
        paid = str(self.request.GET.get('paid', None))
        gender = str(self.request.GET.get('gender', None))
        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))
        context = super(WorkshopRegistrationListView, self).get_context_data(**kwargs)
        save = False
        if paid == 'True':
            context['object_list'] = WorkshopRegistration.objects.filter(workshop=workshop, paid=True)
        elif paid == 'False':
            context['object_list'] = WorkshopRegistration.objects.filter(workshop=workshop, paid=False)
        elif gender == 'male':
            context['object_list'] = WorkshopRegistration.objects.filter(workshop=workshop, male_or_female='Male')
        elif gender == 'female':
            context['object_list'] = WorkshopRegistration.objects.filter(workshop=workshop, male_or_female='Female')
        else:
            context['object_list'] = WorkshopRegistration.objects.filter(workshop=workshop)
            save = True
        context['save'] = save
        context['object_list'] = context['object_list'].order_by('-date')
        context['workshop_id'] = workshop.id
        return context


class WorkshopRegistrationUpdateView(UpdateView):
    model = WorkshopRegistration

    def post(self, request, *args, **kwargs):
        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))
        workshop_registration_list = WorkshopRegistration.objects.filter(workshop=workshop)
        for workshop_registration in workshop_registration_list:
            workshop_registration.paid = False
            workshop_registration.save()
        for key, value in request.POST.items():
            try:
                workshop_registration_id = int(key)
            except ValueError as verr:
                workshop_registration_id = None  # do job to handle: s does not contain anything convertible to int
            except Exception as ex:
                workshop_registration_id = None  # do job to handle: Exception occurred while converting to int

            if workshop_registration_id and value == 'on':
                workshop_registration = WorkshopRegistration.objects.get(id=workshop_registration_id)
                workshop_registration.paid = True
                workshop_registration.save()

        return redirect(reverse('workshop_registration_list', kwargs={'workshop_id': kwargs.get('workshop_id', None)}))


class WorkshopListView(ListView):
    model = Workshop

    def get_context_data(self, **kwargs):
        context = super(WorkshopListView, self).get_context_data(**kwargs)
        workshop = Workshop.objects.all()
        workshops = []
        for i in workshop:
            reg = WorkshopRegistration.objects.filter(workshop=i)
            if i.number_of_seats is not None:
                num = i.number_of_seats - len(reg)
                if num < 0:
                    num = 0
                workshops.append([i, num])
            else:
                workshops.append([i])

        context['workshops'] = workshops
        return context


class WorkshopFeedbackCreateView(CreateView):
    form_class = FeedbackForm
    template_name = 'base/form.html'
    success_url = '/workshop/feedback/success'

    def get_context_data(self, **kwargs):
        context = super(WorkshopFeedbackCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Feedback Form'
        return context

    def form_valid(self, form):
        workshop = Workshop.objects.get(id=self.kwargs.get('workshop_id', None))
        valid_form = super(WorkshopFeedbackCreateView, self).form_valid(form)
        self.object.workshop = workshop
        self.object.save()
        return valid_form


class WorkshopGalleryListView(ListView):
    model = WorkshopGallery

    def get_context_data(self, **kwargs):
        context = super(WorkshopGalleryListView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


class WorkshopGalleryCreateView(CreateView):
    model = WorkshopGallery
    fields = ['workshop', 'image']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super(WorkshopGalleryCreateView, self).form_valid(form)
        return response

    def post(self, request, *args, **kwargs):
        workshop = Workshop.objects.get(id=self.kwargs['pk'])
        image = request.FILES.get('image')
        WorkshopGallery(workshop=workshop, image=image).save()
        return redirect('image_list', self.kwargs['pk'])


class WorkshopGalleryDeleteView(DeleteView):
    model = WorkshopGallery

    def get_success_url(self):
        return reverse('image_list', kwargs={'pk': self.object.workshop.id})

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(WorkshopGalleryDeleteView, self).post(request, *args, **kwargs)
