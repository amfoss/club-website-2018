# created by Chirath R, chirath.02@gmail.com
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

batch_choices = (
    ('1st year', '1st year'),
    ('2nd year', 'wnd year'),
    ('3rd year', '3rd year'),
    ('4th year', '4t year'),
)


class JoinApplication(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    batch = models.CharField(max_length=100, choices=batch_choices)
    motivation = models.TextField()
    cs_background = models.TextField(blank=True)
    previous_work = models.TextField(blank=True)
    interests = models.TextField()

    date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('join_application_detail', kwargs={'pk', self.id})

    class Meta:
        ordering = ('date',)
