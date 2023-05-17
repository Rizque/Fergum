from django.db import models
from django.contrib.auth.models import User, Group
import uuid


class Profile (models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    GROUP_CHOICES = [(group.name, group.name) for group in Group.objects.all()]
    chosen_group = models.CharField(
        max_length=100, choices=GROUP_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username
