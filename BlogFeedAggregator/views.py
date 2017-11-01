# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Article, Feed
from .forms import FeedForm
from django.shortcuts import redirect

import feedparser
import datetime

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'BlogFeedAggregator/blog.html', {'articles': articles })

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request, 'BlogFeedAggregator/feeds_list.html', {'feeds': feeds})

def new_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)

            existingFeed = Feed.objects.filter(url = feed.url)
            if len(existingFeed) == 0:
                feedData = feedparser.parse(feed.url)

                # Fields
                feed.title = feedData.feed.title
                feed.save()

                for entry in feedData.entries:
                    article = Article()
                    article.title = entry.title
                    article.url = entry.link
                    article.description = entry.description

                    # Image section views created

                    article.href = entry.href.link

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')

                    article.publication_date = dateString
                    article.feed = feed
                    article.save()

            return redirect('BlogFeedAggregator.views.feeds_list')
    else:
        form = FeedForm()
        return render(request, 'BlogFeedAggregator/new_feed.html', {'form': form})
