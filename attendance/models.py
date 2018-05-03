from django.db import models
from django_mysql.models import JSONField


class DailyAttendance(models.Model):
    """
    attendance = { "user_id": 0, "user_id": 1 }
    """
    date = models.DateField()
    attendance = JSONField()

    def __str__(self):
        return str(self.date)


class MonthlyAttendance(models.Model):
    """
    attendance = { "user_id": [1, 7] "user_id": [5, 7] }
    """
    date = models.DateField()
    attendance = JSONField()

    def __str__(self):
        return str(self.date)


class YearlyAttendance(models.Model):
    """
    attendance = { "user_id": [100, 350], "user_id": [200, 300] }
    """
    date = models.DateField()
    attendance = JSONField()

    def __str__(self):
        return str(self.date)
