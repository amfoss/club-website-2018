# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from workshop.views import WorkshopRegistrationListView, WorkshopDetailView, WorkshopRegistrationUpdateView

urlpatterns = [
    url(r'^(?P<workshop_id>[0-9]+)/$', WorkshopDetailView.as_view(), name='workshop_detail'),
    url(r'^(?P<workshop_id>[0-9]+)/register/$', WorkshopRegistrationListView.as_view(), name='workshop_register'),
    url(r'^(?P<workshop_id>[0-9]+)/register/list/$',
        login_required(WorkshopRegistrationListView.as_view()), name='workshop_list'),
    url(r'^(?P<workshop_id>[0-9]+)/register/update/$',
        login_required(WorkshopRegistrationUpdateView.as_view()), name='workshop_update'),
    url(r'^success/$',
        TemplateView.as_view(template_name='workshop/success.html'), name='workshop_registration_success'),
]

