# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView

from workshop.models import Workshop


class HomePageView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['tags'] = tags
        context['events'] = Workshop.objects.filter(start_date_time__gte=now()).order_by('start_date_time')[:5]
        return context


class Contact(View):
    def get(self, request):
        template_name = 'home/contact.html'
        return render(request, template_name)

    def post(self, request):
        subject = 'Message from ' + request.POST.get('name')
        content = "Message from : " + request.POST.get('name') + " <" + request.POST.get('email') + ">\n\n" +\
                  request.POST.get('message')
        to_address_list = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        send_mail(subject, content, 'amritapurifoss@gmail.com', to_address_list, fail_silently=True)
        return render(request, template_name='home/contact.html', context={"is_success": True})


def about (request):
    return render(request, 'home/about.html')


tags = ["Malardalen University", "TU Kaiserslautern", "INRIA", "Motorola Solutions",
        "HP", "VU University", "Synack Inc", "Okta", "Qualcomm", "2M companies Inc",
        "Google", "Flipkart", "CISCO", "Ola", "KTH Swedens"]

