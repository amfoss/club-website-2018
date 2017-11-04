from django.conf.urls import url
from Home.views import HomePageView,  Contact
from Home.views import about

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name="home"),
    url(r'^contact/$', Contact.as_view(), name="contact"),
    url(r'^about/$', about, name="about"),
]
