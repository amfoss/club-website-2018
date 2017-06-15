from django.conf.urls import url

from clubManagement.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'^attendance-report-batch/(?P<year>[0-9]+)/$',
        login_required(YearBatchAttendanceReportView.as_view()),
        name='attendance_report_year_all'
    ),
    url(
        r'^attendance-report-batch/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$',
        login_required(YearBatchAttendanceReportView.as_view()),
        name='attendance_report_year_batch'
    ),
    url(
        r'^attendance-report/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$',
        login_required(YearAttendanceReportView.as_view()),
        name='attendance_report_year'
    ),
    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_month'),
    url(
        r'^attendance-report/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        login_required(DayAttendanceView.as_view()),
        name='attendance_report_day_all'
    ),
    url(
        r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        login_required(DayAttendanceView.as_view()),
        name='attendance_report_day_batch'
    ),
    url(
        r'^attendance-add/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        AttendanceAddView.as_view(),
        name='add_attendance_all'
    ),
    url(
        r'^attendance-add/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        AttendanceAddView.as_view(),
        name='add_attendance_batch'
    ),
]
