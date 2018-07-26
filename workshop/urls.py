# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from workshop.views import WorkshopRegistrationListView, WorkshopDetailView, WorkshopRegistrationUpdateView, \
    WorkshopRegisterFormView, WorkshopListView, WorkshopFeedbackCreateView, WorkshopGalleryCreateView, \
    WorkshopGalleryListView, WorkshopGalleryDeleteView, WorkshopCreateView, WorkshopUpdateView, WorkshopDeleteView

urlpatterns = [
    url(r'^$', WorkshopListView.as_view(), name='workshop_list'),
    url(r'^create/$', login_required(WorkshopCreateView.as_view()), name='workshop_create'),
    url(r'^(?P<workshop_id>[0-9]+)/$', WorkshopDetailView.as_view(), name='workshop_detail'),

    # TODO(2) Fix update and uncomment
    # url(r'^(?P<pk>[0-9]+)/update/$', login_required(WorkshopUpdateView.as_view()), name='workshopdetail_update'),

    url(r'^(?P<pk>[0-9]+)/delete/$', login_required(WorkshopDeleteView.as_view()), name='workshop_delete'),
    url(r'^(?P<workshop_id>[0-9]+)/register/$', WorkshopRegisterFormView.as_view(), name='workshop_register'),
    url(r'^(?P<workshop_id>[0-9]+)/register/list/$',
        login_required(WorkshopRegistrationListView.as_view()), name='workshop_registration_list'),
    url(r'^(?P<workshop_id>[0-9]+)/register/update/$',
        login_required(WorkshopRegistrationUpdateView.as_view()), name='workshop_update'),
    url(r'^success/$',
        TemplateView.as_view(template_name='workshop/success.html'), name='workshop_registration_success'),
    url(r'^(?P<workshop_id>[0-9]+)/feedback/$', WorkshopFeedbackCreateView.as_view(), name='workshop_feedback'),
    url(r'^feedback/success/$',
        TemplateView.as_view(template_name='workshop/success_feedback.html'), name='feedback_success'),
    url(r'^(?P<pk>[0-9]+)/add-image/$', login_required(WorkshopGalleryCreateView.as_view()), name='image_create'),
    url(r'^(?P<pk>[0-9]+)/gallery/$', WorkshopGalleryListView.as_view(), name='image_list'),
    url(r'^image/(?P<pk>[0-9]+)/delete/$', login_required(WorkshopGalleryDeleteView.as_view()), name='image_delete'),
]

