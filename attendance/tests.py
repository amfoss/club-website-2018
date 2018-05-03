from datetime import datetime

from django.test import TestCase

from attendance.models import SSIDName, DailyAttendance


class DailyAttendanceTest(TestCase):
    def setUp(self):
        self.attendance_json = {1: 0, 2: 0}
        self.daily_attendance = DailyAttendance(date=datetime.now().date(), attendance=self.attendance_json)

    def test_add_attendance(self):
        """
        Tests adding daily attendance
        """
        self.assertEqual(DailyAttendance.objects.count(), 0)
        self.daily_attendance.save()
        self.assertEqual(DailyAttendance.objects.count(), 1)

    def test_attendance_to_user_list(self):
        """
        Test retrieval user list
        expected: [ [user, attendance], [user, attendance] ]
        """
        pass


class MonthlyAttendanceTest(TestCase):
    def setUp(self):
        pass

    def test_add_attendance(self):
        """
        Tests adding monthly attendance
        """
        pass

    def test_attendance_to_user_list(self):
        """
        Test retrieval user list
        expected: [ [user, attendance], [user, attendance] ]
        """
        pass

    def test_attendance_to_percentage(self):

        pass


class YearlyAttendanceTest(TestCase):
    def setUp(self):
        pass

    def test_add_attendance(self):
        """
        Tests adding yearly attendance
        """
        pass

    def test_attendance_to_user_list(self):
        """
        Test retrieval user list
        expected: [ [user, attendance], [user, attendance] ]
        """
        pass

    def test_attendance_to_percentage(self):
        pass


class SSIDNameTest(TestCase):
    def setUp(self):
        self.ssid = SSIDName()
        self.ssid.generate_random_name()

    def test_add_attachment(self):
        self.assertEqual(SSIDName.objects.count(), 0)
        self.ssid.save()
        self.assertEqual(SSIDName.objects.count(), 1)

    def test_random_ssid_generator(self):
        name1 = self.ssid.name

        self.ssid.generate_random_name()
        name2 = self.ssid.name

        self.assertNotEqual(name1, name2, "Wifi SSID names should be random")
