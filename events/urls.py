from django.conf.urls import url

from events.forms import EventCreateForm
from events.views import EventCreateView, EventUpdateView, EventImageCreateView,  EventDeleteView, \
    EventImageDeleteView, EventDetailView, EventListView, EventImageListView

urlpatterns = [
    url(r'^$', EventListView.as_view(), name='event'),
    url(r'^(?P<pk>[0-9]+)$', EventDetailView.as_view(), name = "event_detail"),
    url(r'^create/', EventCreateView.as_view(), name = "Event_add"),
    url(r'^update/(?P<pk>[0-9]+)', EventUpdateView.as_view(), name = "Event_edit"),
    url(r'^delete/(?P<pk>[0-9]+)', EventDeleteView.as_view(), name = "event_delete"),
    url(r'^(?P<pk>[0-9]+)/images/$', EventImageListView.as_view(), name='eventimage_list'),
    url(r'^(?P<pk>[0-9]+)/addimage/$', EventImageCreateView.as_view(), name = "eventimage_add"),
    url(r'^eventimage/(?P<pk>[0-9]+)/delete/$', EventImageDeleteView.as_view(), name = "eventimage_delete"),



]