# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

INTERN_CHOICE = (('internship', 'Internship'),
                 ('masters', 'Masters'),
                 ('exchange_student', 'Exchange programme'))

SPEAKER_CHOICE = (('talk', ' Talk'),
                  ('demo', 'Demo'),
                  ('workshop', 'Workshop'),
                  ('paper', 'Paper Presentation'),
                  ('other', 'Other'))


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    magazine = models.CharField(max_length=200)
    publication_date = models.DateField(null=True)
    area = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.user.username + " " + self.magazine

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})


class Contribution(models.Model):
    contribution_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.user.username + ' ' + self.org_name + ' ' + self.contribution_id

    def get_absolute_url(self):
        return reverse('contribution_detail', kwargs={'pk': self.pk})


class Gsoc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    name = models.CharField(max_length=250)
    mentor = models.CharField(max_length=250)
    url = models.URLField(max_length=400)
    description = models.TextField(blank=True)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username + ' ' + self.organization + ' ' + str(self.year)


class Intern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=300)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=INTERN_CHOICE)
    start_data = models.DateField(blank=True)
    end_data = models.DateField(blank=True)
    field = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username + ' ' + self.organisation


class Speaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=SPEAKER_CHOICE)
    conference_name = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    year = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username + " " + self.title


class Contest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest_id = models.BigIntegerField()
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    problems_solved = models.IntegerField()
    ranking = models.BigIntegerField()
    year = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username + " " + self.name


class Scholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username + " " + self.name
