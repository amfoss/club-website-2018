# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
import xlrd, datetime
from clubManagement.models import Team
from achievements.models import Contribution
from projects.models import Project
from registration.forms import UserSignUpForm, UserForm
from registration.models import UserInfo


class UserSignUpView(CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signup_success')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('already_logged_in')
        return super(UserSignUpView, self).get(request, *args, **kwargs)


def login(request,  *args, **kwargs):  # view to handle remember me and login
    if request.method == 'POST':
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
    if request.method == 'GET' and request.user.is_authenticated:
        return redirect('already_logged_in')
    return auth_views.login(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = UserInfo
    form_class = UserForm
    template_name = 'base/form.html'

    def form_valid(self, form):
        response = super(UserUpdateView, self).form_valid(form)
        if form.is_valid():
            user = form.instance.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        user = context['form'].instance.user
        context['form'].fields['first_name'].initial = user.first_name
        context['form'].fields['last_name'].initial = user.last_name
        context['form'].fields['email'].initial = user.email
        context['heading'] = 'Update profile'
        return context

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return redirect('permission_denied')
        return super(UserUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != self.get_object().user:
            return redirect('permission_denied')
        return super(UserUpdateView, self).post(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    model = User
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        try:
            context['user_info'] = UserInfo.objects.get(user=self.get_object())
        except User.DoesNotExist:
            context['error'] = 'No data found for this user!'
        context['teams'] = Team.objects.filter(created_by=self.get_object())
        context['projects'] = Project.objects.filter(created_by=self.get_object())
        return context


class ProfileListView(ListView):
    model = UserInfo
    template_name = 'registration/profile_list.html'
    queryset = UserInfo.objects.order_by('user__first_name')


class AddData(View):


    def get(self, request, **kwargs):
        template_name = 'registration/adduser.html'
        wb = xlrd.open_workbook('/Users/rahulk/projects/fosswebsite/registration/templates/registration/contributions.xls')
        wb.sheet_names()
        sh = wb.sheet_by_index(0)
        name = sh.cell(7,0).value
        bug_id = sh.cell(7,1).value
        org = sh.cell(7,3).value
        link = sh.cell(7,2).value
        desc = sh.cell(7,4).value
        title = 'Test'
        date = datetime.date(year=2014, month=1, day=1)
        Contribution(user=request.user,contribution_id=bug_id,title=title,organisation=org,url=link,description=desc,date=date).save()

        return render(request, template_name)