from django.conf.urls import url

from clubManagement.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'^attendance-report/(?P<year>[0-9]+)/$',
        login_required(YearAttendanceReportView.as_view()),
        name='attendance_report_year_all'
    ),
    url(
        r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$',
        login_required(YearAttendanceReportView.as_view()),
        name='attendance_report_year_batch'
    ),
    url(
        r'^attendance-report-student/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$',
        login_required(YearStudentAttendanceReportView.as_view()),
        name='attendance_report_year'
    ),
    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_month'),
    url(
        r'^attendance/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        AttendanceAddView.as_view(),
        name='add_attendance_all'
    ),
    url(
        r'^attendance/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        AttendanceAddView.as_view(),
        name='add_attendance_batch'
    ),

    url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        MonthAttendanceReportView.as_view(), name='attendance_report_month'),

    url(r'^responsibility/$', ResponsibilityListView.as_view(), name='responsibility'),
    url(r'^responsibility/(?P<pk>[0-9]+)/$', ResponsibilityDetailView.as_view(), name='responsibility_detail'),
    url(r'^responsibility/create/$', ResponsibilityCreateView.as_view(), name='responsibility_create'),
    url(r'^responsibility/(?P<pk>[0-9]+)/update/$', ResponsibilityUpdateView.as_view(), name='responsibility_update'),
    url(r'^responsibility/(?P<pk>[0-9]+)/delete/$', ResponsibilityDeleteView.as_view(), name='responsibility_delete'),
]
