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

from fosswebsite import settings
from .views import Home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^accounts/', include('registration.urls')),
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
