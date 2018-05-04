# created by Chirath R, chirath.02@gmail.com

from django.conf.urls import url
from attendance.views import DailyAttendanceView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(
        r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        login_required(DailyAttendanceView.as_view()),
        name='daily_attendance'
    ),
]