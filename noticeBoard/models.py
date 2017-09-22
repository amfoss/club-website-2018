# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Notice(models.Model):
    user = models.ForeignKey(User)
    startdate = models.DateTimeField(auto_now=False, auto_now_add=False)
    enddate = models.DateTimeField(auto_now=False, auto_now_add=False)
    message = models.TextField(null=True)
    title = models.CharField(max_length=150, null=True)
    url = models.URLField(null=True)


