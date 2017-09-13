from django.views.generic import DetailView, CreateView

from workshop.forms import WorkshopRegistrationForm
from workshop.models import Workshop


class WorkshopDetailView(DetailView):
    model = Workshop
    pk_url_kwarg = 'workshop_id'


class WorkshopRegisterView(CreateView):
    form_class = WorkshopRegistrationForm
    template_name = 'base/form.html'
