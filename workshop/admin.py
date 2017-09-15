from django.contrib import admin

# Register your models here.
from workshop.models import Workshop, WorkshopRegistration

admin.site.register(Workshop)
admin.site.register(WorkshopRegistration)
