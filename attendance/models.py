import random
import string

from django.db import models
from django_mysql.models import JSONField


class DailyAttendance(models.Model):
    """
    attendance = { "2016": {"user_id": [1, s_time, e_time], "user_id": [0, s_time, e_time]}  }
    """
    date = models.DateField()
    attendance = JSONField()

    def __str__(self):
        return str(self.date)


class SSIDName(models.Model):
    name = models.CharField(max_length=30)

    def generate_random_name(self):
        size = random.randint(10, 17)
        chars = string.ascii_lowercase + string.digits
        self.name = ''.join(random.choice(chars) for _ in range(size))

    def __str__(self):
        return self.name
