from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('subcategories/<uuid:category_id>/',
         views.subcategories, name='subcategories'),
    path('services/<uuid:subcategory_id>/', views.services, name='services'),


    #     path('services/category/<uuid:category_id>/',
    #          views.category_services, name='category_services'),
    path('service/<uuid:service_id>/', views.service, name='service'),




    path('delete-workerservice/<str:pk>/',
         views.deleteWorkerService, name='delete-workerservice'),
    path('add-workerservice/', views.addWorkerService, name='add-workerservice'),




]
