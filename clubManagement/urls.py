from django.conf.urls import url

from clubManagement.views import AttendanceAddView, YearAttendanceReportView, MonthAttendanceReportView

urlpatterns = [

    url(r'^attendance-report/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$', YearAttendanceReportView.as_view(), name='attendance_report_day'),

    url(
        r'^attendance-report-batch/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$',
        login_required(YearBatchAttendanceReportView.as_view()),
        name='attendance_report_batch_yearly'
    ),
    url(
        r'^attendance-report/(?P<year>[0-9]+)/(?P<user_id>[0-9]+)/$',
        login_required(YearAttendanceReportView.as_view()),
        name='attendance_report_yearly'
    ),

    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_month'),
    # url(r'^attendance-report/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', AttendanceReportView.as_view(), name='attendance_report_year'),
    url(r'^attendance-add/(?P<batch>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$', AttendanceAddView.as_view(), name='add_attendance'),
]
