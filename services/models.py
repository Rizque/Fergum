from django.db import models
from users.models import Profile
import uuid


class ServiceCategory(models.Model):
    name = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, unique=True,
                                   primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    category = models.ManyToManyField(ServiceCategory)

    hourly_rate_1 = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False)
    hourly_rate_2 = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)

    def __str__(self):
        return self.name


class WorkerService(models.Model):
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
