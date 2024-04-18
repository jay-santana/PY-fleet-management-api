from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework import status

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer
from .schemas import taxis_list_schema, trajectories_list_schema

import json

# Create your views here.
@api_view(['GET'])
def listTaxis(request):
    if request.method == 'GET':
        taxis = Taxis.objects.all()    # Get all objects in Taxis database (It returns a queryset)
        paginator = PageNumberPagination()
        paginator.page_size = 10 #data pagination
        result_page = paginator.paginate_queryset(taxis, request)
        serializer = TaxisSerializer(result_page, many=True)     # Serialize the object data into json (Has a 'many' parameter cause it's a queryset)
        response = paginator.get_paginated_response(serializer.data)
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        # Adding pagination information at the beginning of the response object
        response.data = {**pagination_info, **response.data}
        return response   # Return the serialized data                 
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Esquema personalizado para documentar a visualização de listagem de taxis no Swagger
listTaxis = taxis_list_schema(method='get')(listTaxis)


@api_view(['GET'])
def listTrajectories(request):
    if request.method == 'GET':
        trajectories = Trajectories.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10 #data pagination
        result_page = paginator.paginate_queryset(trajectories, request)
        serializer = TrajectoriesSerializer(result_page, many=True)
        response = paginator.get_paginated_response(serializer.data)
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        # Adding pagination information at the beginning of the response object
        response.data = {**pagination_info, **response.data}
        return response   # Return the serialized data 
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Esquema personalizado para documentar a visualização de listagem de trajetórias no Swagger
listTrajectories = trajectories_list_schema(method='get')(listTrajectories)



# def databaseEmDjango():
# data = User.objects.get(pk='gabriel_nick')          # OBJETO
# data = User.objects.filter(user_age='25')           # QUERYSET
# data = User.objects.exclude(user_age='25')          # QUERYSET
# data.save()
# data.delete()
