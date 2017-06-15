# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from projects.models import Project


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ' '


class TeamMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.user.username + " - " + self.team.name


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")
    date = models.DateField()
    modified_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    attendance = models.BooleanField(default=False)

    def __str__(self):
        if self.attendance:
            return self.user.username + " " + str(self.date) + " - present"
        else:
            return self.user.username + " " + str(self.date) + " - absent"


class Responsibility(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return " "


class StudentResponsibility(models.Model):
    responsibility = models.ForeignKey(Responsibility, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StatusReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(upload_to='status_img/', blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username + " " + self.content[:20] + ".."

    def get_absolute_url(self):
        return " "
