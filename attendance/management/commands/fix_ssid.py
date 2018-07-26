from django.core.management import BaseCommand

from attendance.models import DailyAttendance


class Command(BaseCommand):

    @staticmethod
    def get_year_string(text):
        if text == "1st year":
            return "2017"
        elif text == "2nd year":
            return "2016"
        elif text == "3rd year":
            return "2015"
        elif text == "4th year":
            return "2014"
        else:
            print("Error, wrong date", text)
            exit()

    def handle(self, *args, **kwargs):
        attendance_list = DailyAttendance.objects.all()
        for attendance_item in attendance_list:
            attendance = attendance_item.attendance

            if str(attendance_item.date)== "2018-07-24":
                exit()

            print(attendance_item.date, attendance_item.attendance.keys())

            batch_list = attendance.keys()

            for batch in batch_list:
                attendance[self.get_year_string(batch)] = attendance.pop(batch)

            attendance_item.attendance = attendance
            attendance_item.save()
