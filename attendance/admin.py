from django.contrib import admin

from attendance.models import DailyAttendance, MonthlyAttendance, YearlyAttendance

admin.site.register(DailyAttendance)
admin.site.register(MonthlyAttendance)
admin.site.register(YearlyAttendance)

