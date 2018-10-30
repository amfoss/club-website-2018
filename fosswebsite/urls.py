# created by Chirath R, chirath.02@gmail.com
"""fosswebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import home
    2. Add a URL to urlpatterns:  url(r'^$', home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin

from fosswebsite import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'accounts/', include('registration.urls')),
    path(r'accounts/', include('allauth.urls')),
    path(r'club/', include('clubManagement.urls')),
    path(r'achievements/', include('achievements.urls')),
    path(r'project/', include('projects.urls')),
    path(r'timeline/', include('timeline.urls')),
    path(r'workshop/', include('workshop.urls')),
    path(r'home/', include('Home.urls')),
    path('', include('Home.urls')),
    path(r'BlogFeedAggregator/', include('BlogFeedAggregator.urls')),
    path(r'admissions/', include('admissions.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
