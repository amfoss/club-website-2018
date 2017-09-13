from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Workshop(models.Model):
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User)
    description = models.TextField()
    level = models.CharField(blank=True)
    poster = models.ImageField(upload_to='workshop/poster/', null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name
