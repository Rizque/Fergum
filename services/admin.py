from django.contrib import admin
from .models import Service, ServiceCategory, WorkerService

admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(WorkerService)
