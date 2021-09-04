from django.db import models
from django.contrib.auth.models import AbstractUser


class Notes(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=10000)
    tags = models.CharField(max_length=200, default="General")
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title