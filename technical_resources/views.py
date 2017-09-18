# created by Chirath R <chirath.02@gmail.com>
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from technical_resources.models import Category, Links, Files
from technical_resources.forms import CategoryForm, LinksForm, FilesForm


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        links = Links.objects.filter(category=self.get_object())
        files = Files.objects.filter(category=self.get_object())
        context['links'] = links
        context['files'] = files
        return context


class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name = 'base/form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'New Category'
        context['heading'] = 'Category'
        return context


class CategoryUpdateView(UpdateView):
    form_class = CategoryForm
    template_name = 'base/form.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().name
        context['heading'] = 'Category'
        return context
