from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework import status

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer

import json

# Create your views here.
@api_view(['GET'])
def get_taxis(request):
    if request.method == 'GET':
        taxis = Taxis.objects.all()    # Get all objects in Taxis database (It returns a queryset)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(taxis, request)
        serializer = TaxisSerializer(result_page, many=True)     # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)    
        return paginator.get_paginated_response(serializer.data)   # Return the serialized data                 
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_trajectories(request):
    if request.method == 'GET':
        trajectories = Trajectories.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 #paginação dos dados
        result_page = paginator.paginate_queryset(trajectories, request)
        serializer = TrajectoriesSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# def databaseEmDjango():
# data = User.objects.get(pk='gabriel_nick')          # OBJETO
# data = User.objects.filter(user_age='25')           # QUERYSET
# data = User.objects.exclude(user_age='25')          # QUERYSET
# data.save()
# data.delete()
