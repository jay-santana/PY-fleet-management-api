from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('taxis/', views.listTaxis, name='get_all_taxis'),
    path('trajectories/', views.listTrajectories, name='get_all_trajectories'),
    path('last_taxi_location/', views.last_taxi_locations, name='last_taxi_location'),
]