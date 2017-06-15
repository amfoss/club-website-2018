# -*- coding: utf-8 -*-
from __future__ import unicode_literals



from django.db import models

# Create your models here.


class Event(models.Model):
    Name_of_event = models.CharField(max_length=100)
    Starting_date = models.DateTimeField()
    Ending_date = models.DateTimeField()
    Description = models.TextField(max_length=600)
    Mentor_name = models.CharField(max_length=100)
    Mentor_contact = models.IntegerField(max_length=10)
    Mentor_emailId = models.EmailField()
    Beginner_level = models.BooleanField()
    Prerequisite_needed = models.BooleanField()
    Prerequisite_description = models.TextField()
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return self.Name_of_event




