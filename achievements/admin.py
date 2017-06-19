# -*- coding: utf-8 -*-
# created by Chirath R, chirath.02@gmail.com
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Article)
admin.site.register(Contribution)
admin.site.register(Gsoc)
admin.site.register(Intern)
admin.site.register(Speaker)
admin.site.register(Contest)

