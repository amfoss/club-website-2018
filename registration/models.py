# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from datetime import date


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    signature = models.ImageField(upload_to='signature_pics/', blank=True, null=True)
    small_intro = models.CharField(max_length=300, blank=True)
    intro = models.TextField(blank=True)
    address = models.TextField(max_length=500, blank=True)
    interests = models.TextField(blank=True)
    expertise = models.TextField(blank=True)
    gitHub = models.URLField(blank=True)
    blog = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    email = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    year = models.IntegerField(blank=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    typing_speed = models.IntegerField(blank=True, null=True)
    system_number = models.IntegerField(blank=True, null=True)

    is_mentor = models.BooleanField(default=False)
    is_freelance = models.BooleanField(default=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})


class WorkExperience(models.Model):
    workExp = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    start_date = models.DateField("Date", default=date.today)
    end_date = models.DateField("Date", default=date.today)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    work_description = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.workExp.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})