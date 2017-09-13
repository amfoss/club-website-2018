# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.views.generic import TemplateView

from workshop.views import WorkshopRegistrationListView, WorkshopDetailView

urlpatterns = [
    url(r'^(?P<workshop_id>[0-9]+)/$', WorkshopDetailView.as_view(), name='workshop_detail'),
    url(r'^(?P<workshop_id>[0-9]+)/register/$', WorkshopRegistrationListView.as_view(), name='workshop_register'),
    url(r'^success/$', TemplateView.as_view(template_name='workshop/success.html'), name='workshop_registration_success'),
]

