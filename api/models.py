from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image_url = models.TextField()
    isbn = models.IntegerField()
    price = models.IntegerField()
    quanity = models.IntegerField()

    def __str__(self):
        return self.title