# created by Navaneeth S, navisk13@gmail.com
from django.conf.urls import url

from documents.views import DocumentListView, DocumentCreateView, DocumentDeleteView, DocumentUpdateView

urlpatterns = [
    url(r'^$', DocumentListView.as_view(), name='document'),
    url(r'^create/$', DocumentCreateView.as_view(), name='document_create'),
    url(r'^(?P<pk>[0-9]+)/update/$', DocumentUpdateView.as_view(), name='document_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', DocumentDeleteView.as_view(), name='document_delete'),
]

