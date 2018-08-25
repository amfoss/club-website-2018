# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
# Create your views here
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView

from workshop.models import Workshop
from workshop.forms import ContactForm

class HomePageView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['tags'] = tags
        context['events'] = Workshop.objects.filter(start_date_time__gte=now()).order_by('start_date_time')[:5]
        return context


class Contact(View):
    template_name = 'home/contact.html'
    def get(self, request):
        form = ContactForm()
        if request.user.is_authenticated:
            return redirect("/")
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = ContactForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, context={"is_success": False, 'form': form})
        print(form.cleaned_data)
        subject = 'Message from ' + form.cleaned_data.get('name')
        content = "Message from : " + form.cleaned_data.get('name') + " <" + form.cleaned_data.get('email') + ">\n\n" +\
                  form.cleaned_data.get('message')
        to_address_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        send_mail(subject, content, 'amritapurifoss@gmail.com', to_address_list, fail_silently=True)
        return render(request, self.template_name, context={"is_success": True, 'form': form})


def about (request):
    if not request.user.is_authenticated:
        return render(request, 'home/about.html')
    else:
        return redirect("/")

tags = ["Malardalen University", "TU Kaiserslautern", "INRIA", "Motorola Solutions",
        "HP", "VU University", "Synack Inc", "Okta", "Qualcomm", "2M companies Inc",
        "Google", "Flipkart", "CISCO", "Ola", "KTH Swedens"]
