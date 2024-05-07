from django.contrib import admin
from django.urls import path, include

from .views import viewsLastTaxisLocation, viewsTaxis, viewsTrajectories

urlpatterns = [
    path('taxis/', viewsTaxis.listTaxis, name='get_all_taxis'),
    path('trajectories/', viewsTrajectories.listTrajectories, name='get_all_trajectories'),
    path('lastlocation/', viewsLastTaxisLocation.last_taxis_location, name='get_all_last_location'),
]
