# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='promotion/index.html'), name='foss_intro'),
]