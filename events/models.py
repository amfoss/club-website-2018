# -*- coding: utf-8 -*-
# created by Chirath R, chirath.02@gmail.com
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

LEVEL_CHOICES = (('beginner', 'Beginner'),
                 ('intermediate', 'Intermediate'),
                 ('expert', 'Expert'))


class Event(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=300, blank=True)

    trainer_bio = models.TextField(blank=True)
    no_of_participants = models.IntegerField(blank=True, default=0)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=100)
    prerequisite = models.TextField(blank=True)

    travel = models.TextField(blank=True)
    accommodation = models.TextField(blank=True)
    expense = models.FloatField(blank=True, default=0)
    lab_requirements = models.TextField(blank=True)
    icts_support = models.TextField(blank=True)

    permissions = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/')

    def __str__(self):
        return self.event.name


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.full_name + ' ' + self.event.name
