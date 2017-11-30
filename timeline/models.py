# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class AlumniInfo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=300, blank=True)
    date = models.DateField()
    resume = models.FileField(upload_to='resume/', default='null')

    def __str__(self):
        return self.name
