# created by Navaneeth s, navisk13@gmail.com

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from projects.views import *


urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project_detail'),
    url(r'^create/$', login_required(ProjectCreateView.as_view()), name='project_create'),
    url(r'^(?P<pk>[0-9]+)/add-language/$', login_required(LanguageCreateView.as_view()), name='language_create'),
    url(r'^(?P<pk>[0-9]+)/add-image/$', login_required(ProjectScreenShotCreateView.as_view()), name='image_create'),
    url(r'^(?P<pk>[0-9]+)/gallery/$', ProjectScreenShotListView.as_view(), name='image_list'),
    url(r'^(?P<pk>[0-9]+)/update$', login_required(ProjectUpdateView.as_view()), name='project_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(ProjectDeleteView.as_view()), name='project_delete'),
    url(r'^project-member/(?P<pk>[0-9]+)/delete/$', login_required(ProjectMemberDeleteView.as_view()), name='project_member_delete'),
    url(r'^language/(?P<pk>[0-9]+)/delete/$', login_required(LanguageDeleteView.as_view()), name='language_delete'),
    url(r'^image/(?P<pk>[0-9]+)/delete/$', login_required(ProjectScreenShotDeleteView.as_view()), name='image_delete'),
]
