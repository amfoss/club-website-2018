# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from admissions.views import *

urlpatterns = [
    url(r'^$', ContactView.as_view(), name='foss_intro'),
    url(r'^success/$', TemplateView.as_view(template_name='admissions/success.html'), name='join_success'),
    url(r'^join/$', JoinApplicationCreateView.as_view(), name='join'),
    url(r'^join/list$', login_required(JoinApplicationListView.as_view()), name='join_list'),
    url(r'^join/(?P<pk>[0-9]+)/$', login_required(JoinApplicationDetailView.as_view()), name='join_detail'),
    url(r'^join/(?P<pk>[0-9]+)/update$', login_required(JoinApplicationUpdateView.as_view()), name='join_update'),
    url(r'^join/success/$', TemplateView.as_view(template_name='admissions/success.html'), name='join_success'),
    url(r'^join/mail_all/$', login_required(EmailAllApplicantsView.as_view()), name='join_mail_all'),
]
