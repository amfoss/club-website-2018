# -*- coding: utf-8 -*-
# created by Chirath R, chirath.02@gmail.com
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import *
from .models import *


color_list = [
            'rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)',
            'rgb(153, 102, 255)', 'rgb(201, 203, 207)', '#f44336', '#E91E63', '#9C27B0', '#673AB7', '#3F51B5',
            '#2196F3', '#03A9F4', '#00BCD4', '#009688', '#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107',
            '#FF9800', '#FF5722', '#795548', '#9E9E9E', '#607D8B', '#b71c1c', '#880E4F', '#4A148C', '#311B92',
            '#1A237E', '#0D47A1', '#01579B', '#006064', '#004D40', '#1B5E20', '#33691E', '#827717', '#F57F17',
            '#FF6F00', '#E65100', '#BF360C', '#3E2723', '#212121', '#263238'
        ]

month = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September",
         "October", "November", "December"]

month_num = range(13)

class ArticleListView(ListView):
    """
    list out all the articles as a table, article_list.html
    """
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context["month"] = month
        context["range"] = month_num
        return context


class ArticleDetailView(DetailView):
    """
    Show the detail of the article, pk should be passed in the url. article_detail.html
    """
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True   # To show update and delete button
        return context


class ArticleCreateView(CreateView):
    """
    Creates an article, verifies and saves data to the db. article_form.html
    pk should be provided as url parameter.
    """
    model = Article
    fields = ['title', 'area', 'description', 'magazine', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user  # user foreign key has to be explicitly set with the logged in user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(UpdateView):
    """
    Updates an article, same as CreateView but data will be pre loaded in the form. article_form.html
    pk should be provided as url parameter.
    """
    model = Article
    fields = ['title', 'area', 'description', 'magazine', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')   # error page if not admin or creator of article
        return super(ArticleUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user   # user foreign key has to be explicitly set with the logged in user
        return super(ArticleUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')   # error page if not admin or creator of article
        return super(ArticleUpdateView, self).post(request, *args, **kwargs)


class ArticleDeleteView(DeleteView):
    """
    Deletes a given article, takes pk as parameter in the url.
    """
    model = Article
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('article')   # url to redirect after deleting

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')   # error page if not admin or creator of article
        return super(ArticleDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')   # error page if not admin or creator of article
        return super(ArticleDeleteView, self).post(request, *args, **kwargs)


# Contribution views


class ContributionListView(TemplateView):
    template_name = 'achievements/contribution_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContributionListView, self).get_context_data(**kwargs)
        context['contribution_list'] = Contribution.objects.all().order_by('-date')[:6]
        context["month"] = month
        context["range"] = month_num

        contribution_x = Contribution.objects.order_by().values_list('organisation').distinct()
        contribution_y = []

        for org in contribution_x:
            contribution_y.append(len(Contribution.objects.filter(organisation=org[0])))

        context['contribution_x'] = contribution_x
        context['contribution_y'] = contribution_y
        context['color_list'] = color_list[:len(contribution_x)]

        return context


class ContributionDetailView(DetailView):
    model = Contribution

    def get_context_data(self, **kwargs):
        context = super(ContributionDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context


class ContributionCreateView(CreateView):
    model = Contribution
    fields = ['contribution_id', 'title', 'organisation', 'url', 'description', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContributionCreateView, self).form_valid(form)


class ContributionUpdateView(UpdateView):
    model = Contribution
    fields = ['contribution_id', 'title', 'organisation', 'url', 'description', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContributionUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionUpdateView, self).post(request, *args, **kwargs)


class ContributionDeleteView(DeleteView):
    model = Contribution
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('contribution')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContributionDeleteView, self).post(request, *args, **kwargs)


# GSoc Views
class GsocListView(TemplateView):
    template_name = 'achievements/gsoc_list.html'

    def get_context_data(self, **kwargs):
        context = super(GsocListView, self).get_context_data(**kwargs)
        context['gsoc_list'] = Gsoc.objects.all().order_by('-date')[:6]
        context["month"] = month
        context["range"] = month_num
        gsoc_x = Gsoc.objects.order_by().values_list('organization').distinct()
        gsoc_y = []

        for org in gsoc_x:
            gsoc_y.append(len(Gsoc.objects.filter(organization=org[0])))

        context['gsoc_x'] = gsoc_x
        context['gsoc_y'] = gsoc_y
        context['color_list'] = color_list[:len(gsoc_x)]

        return context


class GsocDetailView(DetailView):
    model = Gsoc

    def get_context_data(self, **kwargs):
        context = super(GsocDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context
      

class GsocCreateView(CreateView):
    model = Gsoc
    fields = ['organization', 'title', 'mentors', 'url', 'description', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GsocCreateView, self).form_valid(form)


class GsocUpdateView(UpdateView):
    model = Gsoc
    fields = ['organization', 'title', 'mentors', 'url', 'description', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(GsocUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GsocUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(GsocUpdateView, self).post(request, *args, **kwargs)


class GsocDeleteView(DeleteView):
    model = Gsoc
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('gsoc')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(GsocDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(GsocDeleteView, self).post(request, *args, **kwargs)

      
# Intern Views

class InternListView(ListView):
    model = Intern

    def get_context_data(self, **kwargs):
        context = super(InternListView, self).get_context_data(**kwargs)
        context["month"] = month
        context["range"] = month_num
        return context

class InternDetailView(DetailView):
    model = Intern

    def get_context_data(self, **kwargs):
        context = super(InternDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context
      
    
class InternCreateView(CreateView):
    model = Intern
    fields = ['organisation', 'title', 'location', 'type', 'date', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(InternCreateView, self).form_valid(form)


class InternUpdateView(UpdateView):
    model = Intern
    fields = ['organisation', 'title', 'location', 'type', 'date', 'description']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(InternUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(InternUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(InternUpdateView, self).post(request, *args, **kwargs)


class InternDeleteView(DeleteView):
    model = Intern
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('intern')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(InternDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(InternDeleteView, self).post(request, *args, **kwargs)

      
# Speaker views
class SpeakerListView(ListView):
    model = Speaker

    def get_context_data(self, **kwargs):
        context = super(SpeakerListView, self).get_context_data(**kwargs)
        context["month"] = month
        context["range"] = month_num
        return context

class SpeakerDetailView(DetailView):
    model = Speaker

    def get_context_data(self, **kwargs):
        context = super(SpeakerDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context
        

class SpeakerCreateView(CreateView):
    model = Speaker
    fields = ['title', 'type', 'conference_name', 'location', 'url', 'date', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SpeakerCreateView, self).form_valid(form)


class SpeakerUpdateView(UpdateView):
    model = Speaker
    fields = ['title', 'type', 'conference_name', 'location', 'url', 'date', 'description']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SpeakerUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerUpdateView, self).post(request, *args, **kwargs)


class SpeakerDeleteView(DeleteView):
    model = Speaker
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('speaker')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(SpeakerDeleteView, self).post(request, *args, **kwargs)


# Contest Views
class ContestListView(ListView):
    model = Contest

    def get_context_data(self, **kwargs):
        context = super(ContestListView, self).get_context_data(**kwargs)
        context["month"] = month
        context["range"] = month_num
        return context

class ContestDetailView(DetailView):
    model = Contest

    def get_context_data(self, **kwargs):
        context = super(ContestDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user == self.get_object().user:
            context['edit_permission'] = True
        return context

      
class ContestCreateView(CreateView):
    form_class = ContestForm
    template_name = 'base/form.html'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContestCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContestCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContestCreateView, self).get_context_data(**kwargs)
        context['heading'] = 'Contest'
        context['title'] = 'Contests'
        return context


class ContestUpdateView(UpdateView):
    form_class = ContestForm
    template_name = 'base/form.html'
    model = Contest

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContestUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestUpdateView, self).get_context_data(**kwargs)
        context['heading'] = 'Contest'
        context['title'] = 'Contests'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContestUpdateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContestUpdateView, self).post(request, *args, **kwargs)


class ContestDeleteView(DeleteView):
    model = Contest
    template_name = 'achievements/confirm_delete.html'
    success_url = reverse_lazy('contest')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContestDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().user):
            redirect('permission_denied')
        return super(ContestDeleteView, self).post(request, *args, **kwargs)


class AchievementListView(TemplateView):
    template_name = 'achievements/achievements_list.html'

    def get_context_data(self, **kwargs):
        context = super(AchievementListView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all().order_by('-date')[:6]
        context['contest_list'] = Contest.objects.all().order_by('-date')[:6]
        context['contribution_list'] = Contribution.objects.all().order_by('-date')[:6]
        context['gsoc_list'] = Gsoc.objects.all().order_by('-date')[:6]
        context['intern_list'] = Intern.objects.all().order_by('-date')[:6]
        context['speaker_list'] = Speaker.objects.all().order_by('-date')[:6]
        context['month'] = month
        context['range'] = month_num
        # contribution graph

        contribution_x = Contribution.objects.order_by().values_list('organisation').distinct()
        contribution_y = []

        for org in contribution_x:
            contribution_y.append(len(Contribution.objects.filter(organisation=org[0])))

        context['contribution_x'] = contribution_x
        context['contribution_y'] = contribution_y
        context['color_list'] = color_list[:len(contribution_x)]

        gsoc_x = Gsoc.objects.order_by().values_list('organization').distinct()
        gsoc_y = []

        for org in gsoc_x:
            gsoc_y.append(len(Gsoc.objects.filter(organization=org[0])))

        context['gsoc_x'] = gsoc_x
        context['gsoc_y'] = gsoc_y
        context['color_list_gsoc'] = color_list[:len(gsoc_x)]

        return context
