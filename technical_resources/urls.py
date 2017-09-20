# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url

from technical_resources.views import *


urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<category>[0-9]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^create/$', CategoryCreateView.as_view(), name='category_create'),
    url(r'^(?P<category>[0-9]+)links/create/$', LinkCreateView.as_view(), name='link_create'),
    url(r'^(?P<category>[0-9]+)files/create/$', FileCreateView.as_view(), name='file_create'),
    url(r'^(?P<category>[0-9]+)/update/$', CategoryUpdateView.as_view(), name='category_update'),
    url(r'^(?P<category>[0-9]+)/links/(?P<pk>[0-9]+)/update/$', LinkUpdateView.as_view(), name='link_update'),
    url(r'^(?P<category>[0-9]+)/links/(?P<pk>[0-9]+)/update/$', LinkCreateView.as_view(), name='file_update'),
]
