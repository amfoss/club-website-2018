# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    intro = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    expertise = models.TextField(blank=True)
    gitHub = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    googlePlus = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    year = models.IntegerField(blank=True)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    typing_speed = models.IntegerField(blank=True, null=True)

    is_mentor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        pk = self.id
        return 'url to %d' % pk
