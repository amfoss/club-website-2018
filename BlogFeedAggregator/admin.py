# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Feed, Article

admin.site.register(Feed)
admin.site.register(Article)
