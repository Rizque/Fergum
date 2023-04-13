from django.urls import path
from . import views

urlpatterns = [
    path('add-property/', views.addProperty, name='add-property'),
]
