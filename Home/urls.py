from django.conf.urls import url
from Home.views import HomePageView, contact

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^contact/$', contact, name="contact"),
]
