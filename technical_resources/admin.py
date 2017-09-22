from django.contrib import admin

from technical_resources.models import Category, Link, File


admin.site.register(Category)
admin.site.register(Link)
admin.site.register(File)
