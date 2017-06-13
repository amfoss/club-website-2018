from django.conf.urls import url
from registration.views import UserSignUpView, UserSignUpSuccess, login

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^signup/$', UserSignUpView.as_view(), name="signup"),
    url(r'^signup/success$', UserSignUpSuccess.as_view(), name="signup_success"),
]