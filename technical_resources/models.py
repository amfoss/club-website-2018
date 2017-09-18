from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='technical_resource/images/')
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})


class Links(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=300)
    link = models.URLField()

    def __str__(self):
        return self.category.name + '-' + self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.category.pk})


class Files(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=300)
    file = models.FileField(upload_to='technical_resource/files/')

    def __str__(self):
        return self.category.name + '-' + self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.category.pk})
