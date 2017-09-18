# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url

from technical_resources.views import *


urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='category_list'),
    url(r'^(?P<pk>[0-9]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^create/$', CategoryCreateView.as_view(), name='category_create'),
    url(r'^(?P<pk>[0-9]+)/update$', CategoryUpdateView.as_view(), name='category_update'),
]
