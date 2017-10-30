# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=false)
