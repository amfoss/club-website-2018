# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import FormView
from clubManagement.models import Attendance
from registration.models import UserInfo


class AttendanceAddView(FormView):
    model = UserInfo
    template_name = 'clubManagement/attendance_add.html'
    users = None
    context = None

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')
        return render(request, self.template_name, self.context)

    def get_context_data(self, **kwargs):
        self.context = super(AttendanceAddView, self).get_context_data(**kwargs)
        year = int(kwargs.get('year', None))
        self.users = UserInfo.objects.filter(year=year)
        self.context['users'] = self.users
        return self.context

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)