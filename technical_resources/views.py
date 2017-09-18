# created by Chirath R <chirath.02@gmail.com>
from django.views.generic import ListView, DetailView, CreateView

from technical_resources.models import Category, Links, Files


class CategoryListView(ListView):
    model = Category


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_object(**kwargs)
        links = Links.objects.filter(category=self.get_object())
        files = Files.objects.filter(category=self.get_object())
        context['links'] = links
        context['links'] = files
        return context


# class CategoryCreateView(CreateView):
#     model = 