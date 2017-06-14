# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from clubManagement.models import Attendance
from registration.models import UserInfo

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
         "October", "November", "December"]

month_num = range(12)


class AttendanceAddView(View):
    template_name = 'clubManagement/attendance_add.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *args, **kwargs):
        year = int(kwargs.get('batch', None))
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        user_info_list = UserInfo.objects.filter(year=year)
        attendance_list = []
        for user_info in user_info_list:
            try:
                attendance = Attendance.objects.get(user=user_info.user, date=d)
            except Attendance.DoesNotExist:
                attendance = Attendance(user=user_info.user,
                                        added_by=User.objects.get(username=self.request.user.username), date=d)
                attendance.save()
            attendance_list.append(attendance)
        return {'attendance_list': attendance_list}

    def post(self, request, *args, **kwargs):
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        attendance_list = Attendance.objects.filter(date=d)
        for i in attendance_list:
            i.attendance = False
            i.save()
        for key in request.POST:
            try:
                user = User.objects.get(username=key)
            except User.DoesNotExist:
                user = None
            if user:
                att = Attendance.objects.get(user=user, date=d)
                att.attendance = True
                att.save()
        return redirect('add_attendance', **kwargs)


class DayAttendanceView(View):
    template_name = 'clubManagement/attendance_daily.html'

    def get(self, request, *args, **kwargs):
        context = {}
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        if not Attendance.objects.filter(date=d).exists():
            context['errors'] = 'No records found'
        else:
            year = int(kwargs.get('batch', None))
            user_info_list = UserInfo.objects.filter(year=year)
            attendance_list = []
            for user_info in user_info_list:
                try:
                    att = Attendance.objects.get(user=user_info.user, date=d)
                    attendance_list.append(att)
                except Attendance.DoesNotExist:
                    pass
            if len(attendance_list) > 0:
                context['attendance_list'] = attendance_list
            else:
                context['errors'] = 'No records found'
        return render(request, self.template_name, context)


class YearAttendanceReportView(View):
    template_name = 'clubManagement/attendance_yearly.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=int(kwargs.get('user_id')))
        att = user.attendance_set.filter(date__year=int(kwargs.get('year')))
        if len(att) > 0:
            month_att = []
            for i in month_num:
                month_att.append(len(att.filter(date__month=(i + 1))))
            context = {'user': user, 'month_att': month_att, 'month': month, 'month_num': month_num,
                       'year': kwargs.get('year')}
        else:
            context = {'errors', 'No records found'}
        return render(request, self.template_name, context)


class YearBatchAttendanceReportView(View):
    template_name = 'clubManagement/attendance_batch_yearly.html'

    def get(self, request, *args, **kwargs):
        user_info_list = UserInfo.objects.filter(year=int(kwargs.get('batch')))
        data = []
        for user_info in user_info_list:
            month_att = []
            total_att = 0
            for i in month_num:
                att_month = len(
                    user_info.user.attendance_set.filter(
                        date__year=int(kwargs.get('year')),
                        date__month=(i + 1),
                        attendance=True
                    )
                )
                total_att += att_month
                month_att.append(att_month)
            data.append([user_info.user, month_att, total_att])
        if len(data) > 0:
            context = {'data': data, 'year': kwargs.get('year')}
        else:
            context = {'errors': 'No data found'}
        return render(request, self.template_name, context)
