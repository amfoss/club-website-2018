from django.conf.urls import url
from registration.views import UserCreateView

urlpatterns = [
    url(r'^signup/$', UserCreateView.as_view(), name="signup")
]