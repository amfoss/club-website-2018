
from django.conf.urls import url

from timeline.views import AlumniListView, AlumniCreateView

urlpatterns = [
    url(r'^$', AlumniListView.as_view(), name="timeline_list"),
    url(r'^create/$', AlumniCreateView.as_view(), name='alumni_create'),
]