# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.views.generic import FormView
from clubManagement.models import Attendance
from registration.models import UserInfo


class AttendanceAddView(FormView):
    model = UserInfo
    template_name = 'clubManagement/attendance_add.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')
        year = int(kwargs.get('year', None))
        users = UserInfo.objects.filter(year=year)
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)