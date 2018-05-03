from datetime import datetime

from django.utils import timezone
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
        if timezone.now().month < 7:
            year -= 1
        for i in range(4):
            batches += [year - i]
        return batches

    def calculate_year(self, year):
        year = timezone.now().year - year
        if timezone.now().month > 7:
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
            return 'Alumni - ' + str(year + timezone.now().year) + ' batch'

    def create_daily_attendance_json_data(self):
        # attendance = { "2016": [[user_id, 0, s_time, e_time], ], "2015": [[user_id, 1, s_time, e_time], ] }
        batch_list = self.get_student_years()
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
            attendance.attendance[year][str(user_info.user.id)][0] = 1  # present
            attendance.attendance[year][str(user_info.user.id)][2] = str(timezone.now().strftime('%X'))  # update end time
            attendance.save()

            at = attendance.attendance[year][str(request.user.id)]
            time_in_lab = datetime.strptime(at[2], '%X') - datetime.strptime(at[1], '%X')

            return Response({"status": "success", "time-in-lab": str(time_in_lab)})
        else:
            return Response({"status": "error"})
