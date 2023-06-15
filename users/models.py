from django.db import models
from django.contrib.auth.models import User, Group
import uuid


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    chosen_group = models.CharField(
        max_length=100, choices=[], blank=True, null=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super(Profile, self).save(*args, **kwargs)

    def get_group_choices(self):
        return [(group.name, group.name) for group in Group.objects.all()]

    def get_chosen_group_choices(self):
        return [(group.name, group.name) for group in Group.objects.filter(name=self.chosen_group)]
