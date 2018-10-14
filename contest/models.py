from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Contest(models.Model):
    name = models.CharField(max_length=500)
    # created_by = models.ForeignKey(User, related_name="created_by")
    overview = models.TextField()
    description = models.TextField(blank=True)
    more_info = models.TextField(blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='contest/poster/', null=True, blank=True)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    prize = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class ContestComment(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.full_name + self.contest.name

class ContestSubmission(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    roll_no = models.CharField(max_length=50)
    course = models.CharField(max_length=300)
    start_date_time = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.full_name + self.contest.name


 #submission
# contest
#name
#rno
#class
#date


# contest submission file

#submission
#file
