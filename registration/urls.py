# created by Chirath R, chirath.02@gmail.com
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from registration.views import UserSignUpView, login, UserUpdateView, ProfileDetailView, ProfileListView, AddData

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^signup/$', UserSignUpView.as_view(), name="signup"),
    url(r'^$', ProfileListView.as_view(), name="profile_list"),
    url(r'^(?P<pk>[0-9]+)/$', ProfileDetailView.as_view(), name="profile"),
    url(r'^(?P<pk>[0-9]+)/update/$', login_required(UserUpdateView.as_view()), name="update_profile"),
    url(
        r'^signup/success/$',
        TemplateView.as_view(template_name='registration/signup_success.html'),
        name="signup_success"
    ),
    url(
        r'^signup/already-logged-in/$',
        TemplateView.as_view(template_name='registration/already_logged_in.html'),
        name="already_logged_in"
    ),
    url(
        r'^permission-denied/$',
        TemplateView.as_view(template_name='registration/permission_denied.html'),
        name="permission_denied"
    ),
    url(
        r'^error/$',
        TemplateView.as_view(template_name='registration/error.html'),
        name="error"
    ),
    url(r'^adddata/$', AddData.as_view()),
]
