# created by Chirath R, chirath.02@gmail.com
"""fosswebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from attendance.views import SSIDNameAPIView, MarkAttendanceAPIView
from clubManagement.views import StatusReportDetailApiView
from fosswebsite import settings
from registration.views import UserViewSet, UserInfoViewSet
from .views import Home


router = routers.DefaultRouter()
router.register(r'status-report', StatusReportDetailApiView)
router.register(r'user', UserViewSet)
router.register(r'user-info', UserInfoViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^accounts/', include('registration.urls')),
    # this file is invisible
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^club/', include('clubManagement.urls')),
    url(r'^foss/', include('promotion.urls')),
    url(r'^achievements/', include('achievements.urls')),
    url(r'^documents/', include('documents.urls')),
    url(r'^project/', include('projects.urls')),
    url(r'^timeline/', include('timeline.urls')),
    url(r'^workshop/', include('workshop.urls')),
    url(r'^notices/', include('noticeBoard.urls')),
    url(r'^resources/', include('technical_resources.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^attendance/', include('attendance.urls')),
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/auth/token/$', obtain_jwt_token),
    url(r'^api/ssid-name/$',  SSIDNameAPIView.as_view()),
    url(r'^api/attendance/mark/$',  MarkAttendanceAPIView.as_view()),
    url(r'^api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
