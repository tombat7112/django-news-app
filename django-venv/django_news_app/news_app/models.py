from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/'