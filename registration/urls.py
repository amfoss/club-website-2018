from django.conf.urls import url
from registration.views import UserSignUpView, UserSignUpSuccess, login, ProfileView

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^profile/$', ProfileView.as_view(), name="profile"),
    url(r'^signup/$', UserSignUpView.as_view(), name="signup"),
    url(r'^signup/success$', UserSignUpSuccess.as_view(), name="signup_success"),
]