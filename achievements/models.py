# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from registration.models import UserInfo
# Create your models here.

ACHIEVEMENT_CHOICE = (('article','Article'),
                      ('contribution','Contribution'),
                      ('gsoc','GSoC'),
                      ('intern','Internship'),
                      ('speaker','Speaker'),
                      ('contest','contest'),
                      ('scholarship', 'Scholarship')
                      ('other','Other'))
INTERN_CHOICE = (('internship','Internship'),
                 ('masters','Masters'),
                 ('exchange student','Exchange programme'))
SPEAKER_CHOICE =(('talk',' Talk'),
                 ('demo','Demo'),
                 ('workshop','Workshop'),
                 ('paper','Paper Presentation'),
                 ('other','Other'))
class Achievement(models.Model):
    achievement_id = models.BigIntegerField( primary_key=True, blank=False, unique=True)
    achieve_type = models.CharField(max_length=15, choices=ACHIEVEMENT_CHOICE)
    username = models.ForeignKey(UserInfo, blank=False, null=False)


class Article(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    magazine_name = models.CharField(max_length=50, blank=False, null=False)
    publication_date = models.DateField(blank=False)


class Contribution(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    bug_id = models.BigIntegerField( blank=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    org_name = models.CharField(max_length=50, blank=False, null=False)
    bug_url = models.URLField(max_length=200, blank=False, null=False)
    bug_description = models.CharField(max_length=200)

    class Meta:
        unique_together = ('bug_id','org_name')


class Gsoc(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    organization = models.CharField(max_length=100, blank=False, null=False)
    project_title = models.CharField(max_length=250, blank=False, null=False)
    mentor_name = models.CharField(max_length=50, blank=False, null=False)
    gsoc_url = models.URLField(max_length=400, blank=False, null=False)


class Intern(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    place = models.CharField(max_length=50, blank=False, null=False)
    intern_type = models.CharField(max_length=16, choices=INTERN_CHOICE, blank=False, null=False)
    period = models.CharField(max_length=25, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)


class Speaker(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    title = models.CharField(max_length=200, blank=False, null=False)
    speaker_type = models.CharField(max_length=15, choices=SPEAKER_CHOICE, blank=False, null=False)
    conference_name = models.CharField(max_length=100, blank=False, null=False)
    speaker_url = models.URLField(max_length=400, blank=False, null=False)
    year = models.BigIntegerField( blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)


class Contest_won(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    contest_id = models.BigIntegerField( primary_key=True, blank=False, null=False)
    contest_name = models.CharField(max_length=100, blank=False, null=False)
    contest_url = models.URLField(max_length=200)
    no_of_problems_solved = models.IntegerField(blank=False, null=False)
    ranking = models.BigIntegerField(blank=False, null=False)
    yr_of_participation = models.BigIntegerField(blank=False, null=False)
    description = models.CharField(max_length=200)


class Scholarship(models.Model):
    achievement_id = models.ForeignKey(Achievement, blank=False, null=False)
    username = models.ForeignKey(UserInfo, blank=False, null=False)
    scholarship_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    year = models.IntegerField(blank=False, null=False)


