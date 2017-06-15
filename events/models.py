# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

LEVEL_CHOICES = (('beginner', 'Beginner'),
                     ('intermediate', 'Intermediate'),
                     ('expert', 'Expert'))


class Event(models.Model):
    name = models.CharField(max_length=300)
    starting_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    description = models.TextField()
    mentor_name = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(choices=LEVEL_CHOICES)
    prerequisite_needed = models.BooleanField()
    prerequisite_description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




