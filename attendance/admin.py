from django.contrib import admin

from attendance.models import DailyAttendance, SSIDName

admin.site.register(DailyAttendance)
admin.site.register(SSIDName)

