# created by Chirath R, chirath.02@gmail.com
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
        r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',
        MonthAttendanceReportView.as_view(),
        name='attendance_report_month'
        ),
    url(
        r'^attendance-report-student/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$',
        login_required(YearStudentAttendanceReportView.as_view()),
        name='attendance_report_year'
    ),
    url(
        r'^attendance/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        login_required(AttendanceAddView.as_view()),
        name='add_attendance_all'
    ),
    url(
        r'^attendance/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        login_required(AttendanceAddView.as_view()),
        name='add_attendance_batch'
    ),

    # Responsibilities
    url(r'^responsibility/$', login_required(ResponsibilityListView.as_view()),
        name='responsibility'),
    url(r'^responsibility/(?P<pk>[0-9]+)/$',
        login_required(ResponsibilityDetailView.as_view()),
        name='responsibility_detail'),
    url(r'^responsibility/create/$',
        login_required(ResponsibilityCreateView.as_view()),
        name='responsibility_create'),
    url(r'^responsibility/(?P<pk>[0-9]+)/update/$',
        login_required(ResponsibilityUpdateView.as_view()),
        name='responsibility_update'),
    url(r'^responsibility/(?P<pk>[0-9]+)/delete/$',
        login_required(ResponsibilityDeleteView.as_view()),
        name='responsibility_delete'),
    url(r'^responsibility-student/(?P<pk>[0-9]+)/delete/$',
        StudentResponsibilityDeleteView.as_view(),
        name='student_responsibility_delete'
        ),

    # Teams
    url(r'^teams/$', TeamListView.as_view(), name='team'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(),
        name='team_detail'),
    url(r'^teams/create/$', login_required(TeamCreateView.as_view()),
        name='team_create'),
    url(r'^teams/(?P<pk>[0-9]+)/update$',
        login_required(TeamUpdateView.as_view()), name='team_update'),
    url(r'^teams/(?P<pk>[0-9]+)/delete/$',
        login_required(TeamDeleteView.as_view()), name='team_delete'),
    url(r'^teams-member/(?P<pk>[0-9]+)/delete/$',
        login_required(TeamMemberDeleteView.as_view()),
        name='team_member_delete'),

    # Status update
    url(r'^status-update/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$',
        login_required(MonthlyStatusUpdateDetailView.as_view()),
        name='monthly-status-update-detail'),
    url(r'^status-update/(?P<day>[0-9]+)/(?P<month>[0-9]+)/(?P<year>[0-9]+)/$',
        login_required(StatusUpdateDetailView.as_view()),
        name='status-update-detail'),


    # index
    url(r'^$', login_required(IndexView.as_view()), name='club'),
]
