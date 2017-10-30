# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Article

def article_list(request):
    articles = Article.objects
    return render(request, 'BlogFeedAggregator/blog.html', {'articles': articles })
