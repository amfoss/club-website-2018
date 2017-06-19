# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url

from achievements.views import *

urlpatterns = [

    # Articles
    url(r'^article/$', ArticleListView.as_view(), name='article'),
    url(r'^article/create/$', ArticleCreateView.as_view(), name='article_create'),
    url(r'^article/(?P<pk>[0-9]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^article/(?P<pk>[0-9]+)/update/$', ArticleUpdateView.as_view(), name='article_update'),
    url(r'^article/(?P<pk>[0-9]+)/delete/$', ArticleDeleteView.as_view(), name='article_delete'),

    # Contributions
    url(r'^contribution/$', ContributionListView.as_view(), name='contribution'),
    url(r'^contribution/create/$', ContributionCreateView.as_view(), name='contribution_create'),
    url(r'^contribution/(?P<pk>[0-9]+)/$', ContributionDetailView.as_view(), name='contribution_detail'),
    url(r'^contribution/(?P<pk>[0-9]+)/update/$', ContributionUpdateView.as_view(), name='contribution_update'),
    url(r'^contribution/(?P<pk>[0-9]+)/delete/$', ContributionDeleteView.as_view(), name='contribution_delete'),

    # speaker
    url(r'^speaker/$', SpeakerListView.as_view(), name='speaker'),
    url(r'^speaker/create/$', SpeakerCreateView.as_view(), name='speaker_create'),
    url(r'^speaker/(?P<pk>[0-9]+)/$', SpeakerDetailView.as_view(), name='speaker_detail'),
    url(r'^speaker/(?P<pk>[0-9]+)/update/$', SpeakerUpdateView.as_view(), name='speaker_update'),
    url(r'^speaker/(?P<pk>[0-9]+)/delete/$', SpeakerDeleteView.as_view(), name='speaker_delete'),

]
