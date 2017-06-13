# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from clubManagement.models import Attendance
from registration.models import UserInfo


class AttendanceAddView(View):
    model = UserInfo
    template_name = 'clubManagement/attendance_add.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *args, **kwargs):
        year = int(kwargs.get('batch', None))
        print(year)
        user_info_list = UserInfo.objects.filter(year=year)
        return {'user_info_list': user_info_list}

    def post(self, request, *args, **kwargs):
        print(request.POST)
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        print(d)
        for key in request.POST:
            try:
                user = User.objects.get(username=key)
            except User.DoesNotExist:
                user = None
            if user and not Attendance.objects.filter(date=d).exists():
                Attendance(user=user, added_by=User.objects.get(username=request.user.username), date=d).save()
        return render(request, self.template_name, {})
