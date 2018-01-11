# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Notice(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    message = models.TextField(max_length=500)
    url = models.URLField(null=True)

    def __str__(self):
        return self.title
