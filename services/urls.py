from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.services, name='services'),
    path('delete-workerservice/<str:pk>/',
         views.deleteWorkerService, name='delete-workerservice'),
    path('add-workerservice/', views.addWorkerService, name='add-workerservice'),


]
