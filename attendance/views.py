from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from django.utils.datetime_safe import date
from django.views.generic.base import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import SSIDName, DailyAttendance
from attendance.serializers import SSIDNameSerializer
from registration.models import UserInfo


class SSIDNameAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a SSID name.
        """
        ssid_name = SSIDName.objects.first()
        serializer = SSIDNameSerializer(ssid_name)
        return Response(data=serializer.data)


class MarkAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_student_years(self):
        batches = []
        year = timezone.now().year
        if timezone.now().month < 8:
            year -= 1
        for i in range(3):
            batches += [year - i]
        print(batches)
        return batches

    def calculate_year(self, year):
        year = timezone.now().year - year
        if timezone.now().month > 6:
            year += 1
        if year > 4:
            year = 4
        if year == 1:
            return '1st year'
        elif year == 2:
            return '2nd year'
        elif year == 3:
            return '3rd year'
        elif year == 4:
            return '4th year'

    def create_daily_attendance_json_data(self):
        # attendance = { "2016": [[user_id, 0, s_time, e_time], ], "2015": [[user_id, 1, s_time, e_time], ] }
        batch_list = self.get_student_years()
        print(batch_list)
        attendance_dict = {}

        for batch in batch_list:
            user_info_list = UserInfo.objects.filter(year=batch).order_by(
                'user__first_name')
            # display the current attendance for this date and batch
            attendance_list_batch = {}
            for user_info in user_info_list:
                user_attendance = [0, str(timezone.now().strftime('%X')), str(timezone.now().strftime('%X'))]
                attendance_list_batch[str(user_info.user.id)] = user_attendance

            # attendance list contains all the Attendance objects of the batch with date = d
            year = self.calculate_year(batch)
            attendance_dict[year] = attendance_list_batch
        return attendance_dict

    def post(self, request, format=None):
        ssid_name = SSIDName.objects.first().name
        if request.data.get('name') == ssid_name:
            attendance, created = DailyAttendance.objects.get_or_create(date=timezone.now().date())
            if created:
                attendance.attendance = self.create_daily_attendance_json_data()
            user_info = UserInfo.objects.get(user=request.user)
            year = self.calculate_year(user_info.year)
            try:
                attendance.attendance[year][str(user_info.user.id)][0] = 1  # present
            except KeyError:
                # Edge case when a new user registers after the attendance gets updated for a day, in that case
                # add that user and mark as present
                attendance.attendance[year][str(user_info.user.id)] = \
                    [1, str(timezone.now().strftime('%X')), str((timezone.now() + timedelta(0, 1)).strftime('%X'))]

            # first time
            if attendance.attendance[year][str(user_info.user.id)][1] == \
                    attendance.attendance[year][str(user_info.user.id)][2]:
                attendance.attendance[year][str(user_info.user.id)][1] = str(timezone.now().strftime('%X'))
            # update end time
            attendance.attendance[year][str(user_info.user.id)][2] = \
                str((timezone.now() + timedelta(0, 1)).strftime('%X'))
            attendance.save()

            at = attendance.attendance[year][str(request.user.id)]
            time_in_lab = datetime.strptime(at[2], '%X') - datetime.strptime(at[1], '%X')

            return Response({"status": "success", "time-in-lab": str(time_in_lab)})
        else:
            return Response({"status": "error"})


def create_daily_attendance_dict(daily_attendance):
    attendance = daily_attendance.attendance
    attendance_dict = {}

    for batch, attendance_b in attendance.items():
        attendance_batch = {}
        for user_id, data in attendance_b.items():
            try:
                user = User.objects.get(id=int(user_id))
                time_in_lab = datetime.strptime(data[2], '%X') - datetime.strptime(data[1], '%X')
                if time_in_lab.total_seconds() != 0:
                    data.append(time_in_lab)
                attendance_batch[user] = data
            except User.DoesNotExist:
                pass
        attendance_dict[batch] = attendance_batch

    return attendance_dict


class DailyAttendanceView(View):
    template_name = 'attendance/attendance-daily.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('permission_denied')
        try:
            d = date(int(kwargs.get('year')), int(kwargs.get('month')),
                     int(kwargs.get('day')))
        except ValueError:
            raise Http404

        daily_attendance = get_object_or_404(DailyAttendance, date=d)
        attendance_dict = create_daily_attendance_dict(daily_attendance)

        # attendance_dict = { "1st year": { user: [present, s_time, e_time], } }
        context = {'attendance_dict': attendance_dict, 'head': d}
        return render(request, self.template_name, context)


def sum_daily_attendance_dict(attendance_list):
    # attendance_dict = { "1st year": { user: [present, total, percentage, total_time, avg time], } }
    attendance_dict = {}

    for daily_attendance in attendance_list:
        attendance = daily_attendance.attendance
        for batch, attendance_b in attendance.items():
            if batch not in attendance_dict:
                attendance_dict[batch] = {}
            for user_id, data in attendance_b.items():
                try:
                    user = User.objects.get(id=user_id)
                    time_in_lab = datetime.strptime(data[2], '%X') - datetime.strptime(data[1], '%X')
                    if user not in attendance_dict[batch]:
                        attendance_dict[batch][user] = [data[0], 1, data[0], time_in_lab, time_in_lab]
                    else:
                        # present count
                        attendance_dict[batch][user][0] += data[0]
                        # total
                        attendance_dict[batch][user][1] += 1
                        # total time in lab
                        attendance_dict[batch][user][3] += time_in_lab

                        # attendance percentage
                        if attendance_dict[batch][user][1] == 0:
                            attendance_dict[batch][user][2] = 0
                        else:
                            attendance_dict[batch][user][2] = \
                                attendance_dict[batch][user][0] * 100 / attendance_dict[batch][user][1]

                        # Avg time per day
                        if attendance_dict[batch][user][0] == 0:
                            attendance_dict[batch][user][4] = attendance_dict[batch][user][3]
                        else:
                            attendance_dict[batch][user][4] = \
                                attendance_dict[batch][user][3] / attendance_dict[batch][user][0]
                except User.DoesNotExist:
                    pass

    return attendance_dict


class MonthlyAttendanceView(View):
    template_name = 'attendance/attendance-sum.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('permission_denied')

        year = int(kwargs.get('year'))
        month = int(kwargs.get('month'))

        attendance_list = DailyAttendance.objects.filter(date__year=year, date__month=month)
        if attendance_list.count() == 0:
            raise Http404
        attendance_dict = sum_daily_attendance_dict(attendance_list)
        context = {'attendance_dict': attendance_dict, 'head': str(year) + " " + str(month)}
        return render(request, self.template_name, context)


class YearlyAttendanceView(View):
    template_name = 'attendance/attendance-sum.html'

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('permission_denied')

        year = int(kwargs.get('year'))

        attendance_list = DailyAttendance.objects.filter(date__year=year)
        if attendance_list.count() == 0:
            raise Http404
        attendance_dict = sum_daily_attendance_dict(attendance_list)
        context = {'attendance_dict': attendance_dict, 'head': str(year)}
        return render(request, self.template_name, context)
