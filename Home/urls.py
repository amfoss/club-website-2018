from django.conf.urls import url
from Home.views import HomePageView, contact
from Home.views import about

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^contact/$', contact, name="contact"),
    url(r'^about/$', about, name="about"),
]
