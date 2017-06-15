from django.conf.urls import url
from registration.views import UserSignUpView, UserSignUpSuccess, login, ProfileView

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^(?P<pk>\d+)$', ProfileView.as_view(template_name = 'profile/profile.html'), name="profile"),
    url(r'^signup/$', UserSignUpView.as_view(), name="signup"),
    url(r'^signup/success$', UserSignUpSuccess.as_view(), name="signup_success"),
]