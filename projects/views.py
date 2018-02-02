# created by Navaneeth S, navisk13@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

from projects.models import Project, ProjectMember, Language, ProjectScreenShot
from django.urls import reverse, reverse_lazy


class ProjectListView(ListView):
    model = Project


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project_list'] = self.get_object().projectmember_set.all()
        context['user_count'] = len(context['project_list'])
        context['all_users'] = User.objects.all()
        context['languages'] = Language.objects.filter(project=Project.objects.get(id=self.kwargs['pk']))
        if self.request.user.is_superuser or self.request.user == self.object.created_by:
            context['edit_permission'] = True
        else:
            context['edit_permission'] = False
        return context

    def post(self, request,  **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            return redirect('permission_denied')
        try:
            user = User.objects.get(id=int(request.POST.get('user_id')))
            ProjectMember.objects.get(project=self.get_object(), user=user)
        except ProjectMember.DoesNotExist:
            try:
                user = User.objects.get(id=int(request.POST.get('user_id')))
                ProjectMember(project=self.get_object(), user=user).save()
            except User.DoesNotExist:
                redirect('error')
        return redirect('project_detail', self.get_object().pk)


class ProjectCreateView(CreateView):
    model = Project
    fields = ['title', 'url', 'image', 'description', 'date']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super(ProjectCreateView, self).form_valid(form)
        ProjectMember(project=self.object, user=self.request.user).save()
        return response


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['title', 'url', 'image', 'description', 'date']

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectUpdateView, self).post(request, *args, **kwargs)


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project')

    def get(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectDeleteView, self).post(request, *args, **kwargs)


class ProjectMemberDeleteView(DeleteView):
    model = ProjectMember

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.id})

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectMemberDeleteView, self).post(request, *args, **kwargs)


class LanguageCreateView(CreateView):
    model = Language
    fields = ['language', 'project']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super(LanguageCreateView, self).form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super(LanguageCreateView, self).get_context_data(**kwargs)
        project = Project.objects.get(id=self.kwargs['pk'])
        context['proj'] = project
        return context

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['pk'])
        language = request.POST.get('language')
        Language(project=project, language=language).save()
        return redirect('project_detail', self.kwargs['pk'])


class LanguageDeleteView(DeleteView):
    model = Language

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.id})

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(LanguageDeleteView, self).post(request, *args, **kwargs)


class ProjectScreenShotListView(ListView):
    model = ProjectScreenShot

    def get_context_data(self, **kwargs):
        context = super(ProjectScreenShotListView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['pk']
        return context


class ProjectScreenShotCreateView(CreateView):
    model = ProjectScreenShot
    fields = ['project', 'image']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super(ProjectScreenShotCreateView, self).form_valid(form)
        return response

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['pk'])
        image = request.FILES.get('image')
        ProjectScreenShot(project=project, image=image).save()
        return redirect('screenshot_list', self.kwargs['pk'])


class ProjectScreenShotDeleteView(DeleteView):
    model = ProjectScreenShot

    def get_success_url(self):
        return reverse('screenshot_list', kwargs={'pk': self.object.project.id})

    def post(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user == self.get_object().created_by):
            redirect('permission_denied')
        return super(ProjectScreenShotDeleteView, self).post(request, *args, **kwargs)

