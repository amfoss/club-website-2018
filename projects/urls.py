# created by Navaneeth s, navisk13@gmail.com

from django.conf.urls import url
from projects.views import *


urlpatterns=[
    url(r'^$', ProjectListView.as_view(), name='project'),
    url(r'^(?P<pk>[0-9]+)/$', ProjectDetailView.as_view(), name='project_detail'),
    url(r'^create/$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^(?P<pk>[0-9]+)/update$', ProjectUpdateView.as_view(), name='project_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProjectDeleteView.as_view(), name='project_delete'),
    url(r'^project-member/(?P<pk>[0-9]+)/delete/$', ProjectMemberDeleteView.as_view(), name='project_member_delete'),

    ]