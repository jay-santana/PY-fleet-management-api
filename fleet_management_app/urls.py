from django.contrib import admin
from django.urls import path, include

from .views import viewsTaxis, viewsTrajectories, viewsLastTaxisLocation 

urlpatterns = [
    path('taxis/', viewsTaxis.listTaxis, name='get_all_taxis'),
    path('trajectories/', viewsTrajectories.listTrajectories, name='get_all_trajectories'),
    path('lastlocation/', viewsLastTaxisLocation.lastTaxisLocation, name='get_all_last_location'),
]
