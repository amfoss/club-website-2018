from django.contrib import admin

# Register your models here.
from workshop.models import Workshop, WorkshopRegistration, WorkshopFeedback

admin.site.register(Workshop)
admin.site.register(WorkshopRegistration)
admin.site.register(WorkshopFeedback)
