from django.contrib.auth.models import User
from django.db import models


class Workshop(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    overview = models.TextField()
    course_details = models.TextField(blank=True)
    project = models.TextField(blank=True)
    other_info = models.TextField(blank=True)
    level = models.CharField(blank=True, max_length=100)
    number_of_seats = models.IntegerField()
    poster = models.ImageField(upload_to='workshop/poster/', null=True, blank=True)
    start_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(Workshop, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    roll_number = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    hostel_details = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=50, blank=True)
    section = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + self.batch


class WorkshopGallery(models.Model):
    workshop = models.ForeignKey(Workshop)
    image = models.ImageField(upload_to='workshop/images/')
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.workshop.name


class WorkshopFeedback(models.Model):
    workshop = models.ForeignKey(Workshop, null=True)
    name = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.name + ' ' + self.workshop.name
