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
        """
        A view for an admin to add attendance for a particular date.
        url = /batch/year/month/day/
        date is calculated from (year, month, day)
        and students is selected according to batch
        """
        if not request.user.is_superuser:
            return redirect('permission_denied')
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        year = int(kwargs.get('batch', None))
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        user_info_list = UserInfo.objects.filter(year=year)
        attendance_list = []

        # display the current attendance for this date and batch

        for user_info in user_info_list:
            try:
                attendance = Attendance.objects.get(user=user_info.user, date=d)
            except Attendance.DoesNotExist:
                attendance = Attendance(user=user_info.user,
                                        added_by=User.objects.get(username=self.request.user.username), date=d)
                attendance.save()
            attendance_list.append(attendance)
        # attendance list contains all the Attendance objects of the batch with date = d
        return {'attendance_list': attendance_list, 'head': str(d)}

    def post(self, request, **kwargs):
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        attendance_list = Attendance.objects.filter(date=d)

        # make all attendance false and make attendance = true for users in request.POST.

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
    """
    A view to view a attendance by date.
    url = /batch/year/month/day/
    date is calculated from (year, month, day) and students is selected according to batch
    """
    template_name = 'clubManagement/attendance_daily.html'

    def get(self, request, **kwargs):
        """
        find all attendance where user has year=batch and date=d
        """
        context = {}
        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        if not Attendance.objects.filter(date=d).exists():
            context['errors'] = 'No records found'
        else:
            user_info_list = UserInfo.objects.filter(year=int(kwargs.get('batch')))
            attendance_list = []
            for user_info in user_info_list:
                # attendance associated with the user whose year=batch and date=d
                att = user_info.user.attendance_set.filter(date=d)
                if att.exists():
                    attendance_list += att
            if len(attendance_list) > 0:
                context['attendance_list'] = attendance_list
            else:
                context['errors'] = 'No records found'
            context['head'] = str(d)
        return render(request, self.template_name, context)


class YearAttendanceReportView(View):
    template_name = 'clubManagement/attendance_yearly.html'

    def get(self, request, **kwargs):
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

    def get(self, request, **kwargs):
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
            context = {'data': data, 'head': kwargs.get('year')}
        else:
            context = {'errors': 'No data found'}
        return render(request, self.template_name, context)


class MonthAttendanceReportView(View):
    template_name = 'clubManagement/attendance_monthly.html'

    def get(self, request, *args, **kwargs):
        context = {}
        if 'user_id' in kwargs:
            user = User.objects.get(id=int(kwargs.get('user_id')))
            att = user.attendance_set.filter(date__month=int(kwargs.get('month'), date_year=int(kwargs.get('year'))))
            day_att = []
            if date.month == 1:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 2:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29"]
                day_num = range(29)
            if date.month == 3:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 4:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                day_num = range(30)

            if date.month == 5:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 6:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                day_num = range(30)
            if date.month == 7:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 8:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 9:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                day_num = range(30)
            if date.month == 10:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)
            if date.month == 11:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
                day_num = range(30)
            if date.month == 12:
                day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]
                day_num = range(31)

            for i in day_num:
                day_att.append(len(att.filter(date__day=(i+1))))
                context = {'user': user, 'day_att': day_att, 'day': day, 'day_num': day_num, 'month': kwargs.get('month')}
        return render(request, self.template_name, context)
