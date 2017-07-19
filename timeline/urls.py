
from django.conf.urls import url

from timeline.views import AlumniListView

urlpatterns = [
    url(r'^$', AlumniListView.as_view(), name="timeline_list"),
]