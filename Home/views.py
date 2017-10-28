# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home/home.html"

def contact(request):
    return render(request, 'home/contact.html')

def about (request):
    return render(request, 'home/about.html')
