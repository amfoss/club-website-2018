from django.conf.urls import url

from clubManagement.views import AttendanceAddView, YearAttendanceReportView, TeamListView, TeamDetailView, \
    MemberDeleteView, TeamDeleteView, TeamUpdateView

urlpatterns = [
    url(r'^attendance-report/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$', YearAttendanceReportView.as_view(), name='attendance_report_day'),
    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_month'),
    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_year'),
    url(r'^attendance-add/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', AttendanceAddView.as_view(), name='add_attendance'),
    url(r'^teams/$', TeamListView.as_view(), name='view_teams'),
    url(r'^teams/(?P<pk>[0-9]+)/$', TeamDetailView.as_view(), name='team_detail'),
    url(r'^teams/delmemb/(?P<pk>[0-9]+)/', MemberDeleteView.as_view(), name='delete_member'),
    url(r'^teams/delete/(?P<pk>[0-9]+)/', TeamDeleteView.as_view(), name='delete_team'),
    url(r'^teams/edit/(?P<pk>[0-9]+)/', TeamUpdateView.as_view(), name='edit_team')
]
