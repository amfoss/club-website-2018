from django.contrib import admin

from attendance.models import DailyAttendance, MonthlyAttendance, YearlyAttendance, SSIDName

admin.site.register(DailyAttendance)
admin.site.register(MonthlyAttendance)
admin.site.register(YearlyAttendance)
admin.site.register(SSIDName)

