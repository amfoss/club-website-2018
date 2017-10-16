from django.conf.urls import url

from events.forms import EventCreateForm
from events.views import EventCreateView, EventUpdateView

urlpatterns = [
    url(r'^create/', EventCreateView.as_view(), name = "Event_add"),
    url(r'^edit/', EventUpdateView.as_view(), name = "Event_edit"),

]