# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Project)
admin.site.register(ProjectMembers)
admin.site.register(ProjectScreenShot)
admin.site.register(Language)
