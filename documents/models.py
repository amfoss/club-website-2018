# created by Navaneeth S, navisk13@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Document(models.Model):
    user = models.ForeignKey(User)
    document = models.FileField(upload_to='files/')
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)

