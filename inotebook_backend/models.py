from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=10000)
    tags = models.CharField(max_length=200, default="General")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title