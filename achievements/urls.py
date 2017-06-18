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

]
