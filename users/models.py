from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    # def __str__(self):
    #     return self.name
