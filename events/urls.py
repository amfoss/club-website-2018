from django.conf.urls import url

from events.forms import EventCreateForm
from events.views import EventCreateView, EventUpdateView, EventImageCreateView, EventImageUpdateView, EventDeleteView, \
    EventImageDeleteView, EventDetailView

urlpatterns = [
    url(r'^create/', EventCreateView.as_view(), name = "Event_add"),
    url(r'^edit/(?P<pk>[0-9]+)', EventUpdateView.as_view(), name = "Event_edit"),
    url(r'^addimage/', EventImageCreateView.as_view(), name = "eventimage_add"),
    url(r'^event/(?P<pk>[0-9]+)', EventDetailView.as_view(), name = "event_detail"),
    url(r'^editimage/(?P<pk>[0-9]+)', EventImageUpdateView.as_view(), name = "eventimage_edit"),
    url(r'^deleteimage/(?P<pk>[0-9]+)/', EventDeleteView.as_view(), name = "eventimage_delete"),
    url(r'^delete/(?P<pk>[0-9]+)', EventImageDeleteView.as_view(), name = "event_delete"),


]