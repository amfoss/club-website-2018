import csv
from datetime import date
from django.core.management import BaseCommand

from clubManagement.models import Attendance
from registration.models import UserInfo


def get_active_users():
    start_year = date.today().year

    if date.today().month < 8:
        start_year -= 1

    user_data = {}

    for year in range(start_year, start_year - 4, -1):
        user_info_list = UserInfo.objects.filter(year=year)
        user_list = []
        for user_info in user_info_list:
            if user_info.user.is_active and not user_info.is_mentor:
                user_list.append(user_info.user)

        if user_list:
            user_data[year] = user_list

    return user_data


def return_location_date_user_list(date_user_list, date):
    i = 0
    for date_user in date_user_list:
        if date_user[0] == date:
            return i
        i += 1
    date_user_list.append([date, []])
    return i


class Command(BaseCommand):
    help = 'Command to convert status update to csv'

    def handle(self, *args, **options):
        user_list_dict = get_active_users()

        for year, user_list in user_list_dict.items():
            date_user_list = []

            for user in user_list:
                attendance_list = Attendance.objects.filter(user=user).\
                    order_by('date')

                for attendance in attendance_list:
                    index = return_location_date_user_list(
                        date_user_list, attendance.date)
                    if attendance.attendance:
                        date_user_list[index][1].append(user)

            field_names = ['Name']

            with open(str(year) + '.csv', 'w') as file:
                write = csv.writer(file)

                sorted(date_user_list, key=lambda data: data[0])

                for date_user in date_user_list:
                    field_names.append(str(date_user[0]))

                write.writerow(field_names)

                for user in user_list:
                    row_data = [user.get_full_name()]
                    for date_user in date_user_list:
                        if user in date_user[1]:
                            row_data.append('Y')
                        else:
                            row_data.append('N')

                    write.writerow(row_data)









