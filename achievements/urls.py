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

    # GSoc
    url(r'^gsoc/$', GsocListView.as_view(), name='gsoc'),
    url(r'^gsoc/create/$', GsocCreateView.as_view(), name='gsoc_create'),
    url(r'^gsoc/(?P<pk>[0-9]+)/$', GsocDetailView.as_view(), name='gsoc_detail'),
    url(r'^gsoc/(?P<pk>[0-9]+)/update/$', GsocUpdateView.as_view(), name='gsoc_update'),
    url(r'^gsoc/(?P<pk>[0-9]+)/delete/$', GsocDeleteView.as_view(), name='gsoc_delete'),

    # Intern
    url(r'^intern/$', InternListView.as_view(), name='intern'),
    url(r'^intern/create/$', InternCreateView.as_view(), name='intern_create'),
    url(r'^intern/(?P<pk>[0-9]+)/$', InternDetailView.as_view(), name='intern_detail'),
    url(r'^intern/(?P<pk>[0-9]+)/update/$', InternUpdateView.as_view(), name='intern_update'),
    url(r'^intern/(?P<pk>[0-9]+)/delete/$', InternDeleteView.as_view(), name='intern_delete'),

    # speaker
    url(r'^speaker/$', SpeakerListView.as_view(), name='speaker'),
    url(r'^speaker/create/$', SpeakerCreateView.as_view(), name='speaker_create'),
    url(r'^speaker/(?P<pk>[0-9]+)/$', SpeakerDetailView.as_view(), name='speaker_detail'),
    url(r'^speaker/(?P<pk>[0-9]+)/update/$', SpeakerUpdateView.as_view(), name='speaker_update'),
    url(r'^speaker/(?P<pk>[0-9]+)/delete/$', SpeakerDeleteView.as_view(), name='speaker_delete'),

    # Contest
    url(r'^contest/$', ContestListView.as_view(), name='contest'),
    url(r'^contest/create/$', ContestCreateView.as_view(), name='contest_create'),
    url(r'^contest/(?P<pk>[0-9]+)/$', ContestDetailView.as_view(), name='contest_detail'),
    url(r'^contest/(?P<pk>[0-9]+)/update/$', ContestUpdateView.as_view(), name='contest_update'),
    url(r'^contest/(?P<pk>[0-9]+)/delete/$', ContestDeleteView.as_view(), name='contest_delete'),

    # all achievements
    url(r'^$', AchievementListView.as_view(), name='achievements')
]
