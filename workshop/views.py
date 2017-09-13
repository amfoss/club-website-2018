from django.views.generic import DetailView, CreateView

from workshop.forms import WorkshopForm
from workshop.models import Workshop


class WorkshopDetailView(DetailView):
    model = Workshop


class WorkshopRegisterView(CreateView):
    form_class = WorkshopForm
    template_name = 'base/form.html'
