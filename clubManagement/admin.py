# -*- coding: utf-8 -*-
# created by Chirath R, chirath.02@gmail.com
from __future__ import unicode_literals

from django.contrib import admin
from clubManagement.models import Attendance, Team, Responsibility, TeamMember, \
    StatusUpdate

admin.site.register(Attendance)
admin.site.register(Team)
admin.site.register(Responsibility)
admin.site.register(TeamMember)
admin.site.register(StatusUpdate)
