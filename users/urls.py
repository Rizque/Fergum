from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('select-group/', views.selectGroup, name='select-group'),
    path('add-group/', views.add_group, name='add_group'),
    path('switch-group/', views.switch_group, name='switch_group'),



    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),


    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('adress/', views.adress, name='adress'),
    # path('properties/', views.property_list, name='property_list'),
    path('property=<uuid:pk>/', views.mainProperty, name='main-property'),
    path('service/', views.mainService, name='main-service'),

    path('home/', views.home, name='home'),





]
