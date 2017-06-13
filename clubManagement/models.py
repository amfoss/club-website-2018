# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")
    date = models.DateTimeField()
    modified_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.username + " " + str(self.date)


class Responsibility(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responsibility = models.CharField(max_length=300)
    more_info = models.TextField(blank=True)

    def __str__(self):
        return self.user.username + " " + self.responsibility

    def get_absolute_url(self):
        return " "


class StatusReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    img = models.ImageField(upload_to='status_img/', blank=True)
    # project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username + " " + self.content[:20] + ".."

    def get_absolute_url(self):
        return " "
