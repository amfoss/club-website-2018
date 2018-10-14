# created by Navaneeth S, navisk13@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    document = models.FileField(upload_to='files/')
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
