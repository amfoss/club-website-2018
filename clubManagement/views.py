# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from clubManagement.models import Attendance
from registration.models import UserInfo

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
         "October", "November", "December"]

month_num = range(12)


def calculate_year(year):
    if datetime.now().month > 5:
        year += 1

    if year == 1:
        return '1st year'
    elif year == 2:
        return '2nd year'
    elif year == 3:
        return '3rd year'
    elif year == 4:
        return '4th year'
    else:
        return 'Alumni - ' + str(year) + ' batch'


class AttendanceAddView(View):
    template_name = 'clubManagement/attendance_add.html'

    def get(self, request, **kwargs):
        """
        A view for an admin to add attendance for a particular date.
        url = /batch/year/month/day/
        date is calculated from (year, month, day)
        and students is selected according to batch

        attendance_list = [ [ '1st_year', list_of_1st_years ], ..... ]
        """
        if not request.user.is_superuser:
            return redirect('permission_denied')

        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))
        context = {}
        if 'batch' in kwargs:
            user_info_list = UserInfo.objects.filter(year=int(kwargs.get('batch')))
            attendance_list_year = []

            # display the current attendance for this date and batch

            for user_info in user_info_list:
                try:
                    attendance = Attendance.objects.get(user=user_info.user, date=d)
                except Attendance.DoesNotExist:
                    attendance = Attendance(user=user_info.user,
                                            added_by=User.objects.get(username=self.request.user.username), date=d)
                    attendance.save()
                attendance_list_year.append(attendance)

            # attendance list contains all the Attendance objects of the batch with date = d
            year = calculate_year(int(kwargs.get('batch')) - datetime.now().year)
            context = {'attendance_list': [attendance_list_year, year]}
        else:
            pass
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        if not request.user.is_superuser:
            return redirect('permission_denied')

        d = date(int(kwargs.get('year')), int(kwargs.get('month')), int(kwargs.get('day')))

        if 'batch' in kwargs:
            user_info_list = UserInfo.objects.filter(year=int(kwargs.get('batch')))
            for user_info in user_info_list:
                attendance_list = user_info.user.attendance_set.filter(date=d)
                for i in attendance_list:
                    i.attendance = False
                    i.save()
        else:
            # make all attendance false and make attendance = true for users in request.POST.
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
