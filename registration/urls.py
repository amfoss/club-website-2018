from django.conf.urls import url
from django.views.generic import TemplateView
from registration.views import UserSignUpView, login

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^signup/$', UserSignUpView.as_view(), name="signup"),
    url(
        r'^signup/success$',
        TemplateView(template_name='registration/signup_success.html').as_view(),
        name="signup_success"
    ),
    url(
        r'^signup/already-logged-in',
        TemplateView(template_name='registration/already_logged_in.html').as_view(),
        name="already_logged_in"
    ),
    url(
        r'^signup/permission-denied',
        TemplateView(template_name='registration/permission-denied.html').as_view(),
        name="permission_denied"
    ),
]
