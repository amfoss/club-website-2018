from django.conf.urls import url

from clubManagement.views import AttendanceAddView

urlpatterns = [
    url(r'^add/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', AttendanceAddView.as_view(), name='add_attendance'),
]
