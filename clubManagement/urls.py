from django.conf.urls import url

from clubManagement.views import AttendanceAddView

urlpatterns = [
    url(r'^add/$', AttendanceAddView.as_view(), name='add-attendance'),
]
