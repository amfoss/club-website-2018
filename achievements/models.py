# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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
                 ('exchange_student','Exchange programme'))
SPEAKER_CHOICE =(('talk',' Talk'),
                 ('demo','Demo'),
                 ('workshop','Workshop'),
                 ('paper','Paper Presentation'),
                 ('other','Other'))


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    magazine_name = models.CharField(max_length=50)
    publication_date = models.DateField()
    def __str__(self):
        return self.user.username + " " + self.magazine_name

class Contribution(models.Model):
    bug_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=50)
    bug_url = models.URLField(max_length=200)
    bug_description = models.CharField(max_length=500)

    class Meta:
        unique_together = ('bug_id','org_name')

    def __str__(self):
        return self.user.username



class Gsoc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100)
    project_title = models.CharField(max_length=250)
    mentor_name = models.CharField(max_length=50)
    gsoc_url = models.URLField(max_length=400)

    def __str__(self):
        return self.user.username



class Intern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=50)
    intern_type = models.CharField(max_length=16)
    period = models.CharField(max_length=25)
    area = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username



class Speaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    speaker_type = models.CharField(max_length=15)
    conference_name = models.CharField(max_length=100)
    speaker_url = models.URLField(max_length=400)
    year = models.BigIntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username + " " + self.title



class Contest_won(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest_id = models.BigIntegerField()
    contest_name = models.CharField(max_length=100)
    contest_url = models.URLField(max_length=200)
    no_of_problems_solved = models.IntegerField()
    ranking = models.BigIntegerField()
    yr_of_participation = models.BigIntegerField()
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.user.username + " " + self.contest_name



class Scholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    year = models.IntegerField()

    def __str__(self):
        return self.user.username + " " + self.scholarship_name

