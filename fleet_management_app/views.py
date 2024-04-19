from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer
from .schemas import taxis_list_schema, trajectories_list_schema

import json

# Create your views here.
from django.db.models import Q

# Function to filter taxis
def filter_taxis(taxis, filter_by):
    if filter_by is not None:
        # Check if it's a number (ID) or plate
        if filter_by.isdigit():  # If it's a number, assume it's the ID
            return taxis.filter(id=int(filter_by))
        else:  # If it's not a number, assume it's the plate
            return taxis.filter(plate__icontains=filter_by)
    return taxis

# Function to order taxis
def sort_taxis(taxis, sort_by):
    if sort_by is not None:
        return taxis.order_by('-' + sort_by[1:] if sort_by.startswith('-') else sort_by)
    return taxis

# Function to search for taxis
def search_taxis(taxis, search):
    if search is not None:
        return taxis.filter(Q(id__icontains=search) | Q(plate__icontains=search))
    return taxis

# Function to get the page size of a request
def get_page_size(request):
    page_size = request.query_params.get('page_size', 10)
    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 10
    return page_size

# Function to get the page number of a request
def get_page_number(request):
    page_number = request.query_params.get('page', 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
    return page_number

# Function to list all taxis
@api_view(['GET'])
def listTaxis(request):
    """
    List all taxis with optional filtering, sorting, searching, and pagination.
    """
    if request.method == 'GET':
        # Get request query parameters
        filter_by = request.query_params.get('filter_by', None)
        sort_by = request.query_params.get('sort_by', None)
        search = request.query_params.get('search', None)

        # Get page size and page number
        page_size = get_page_size(request)
        page_number = get_page_number(request)

        # Filter, sort, and search taxis
        taxis = Taxis.objects.all()
        taxis = filter_taxis(taxis, filter_by)
        taxis = sort_taxis(taxis, sort_by)
        taxis = search_taxis(taxis, search)
        
        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(taxis, request)
        
        # Serialize the paginated queryset
        serializer = TaxisSerializer(result_page, many=True)
        
        # Construct response data
        response = paginator.get_paginated_response(serializer.data)
        
        # Add current_page and total_pages
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        response.data = {**pagination_info, **response.data}
        
        return response

    return Response(status=status.HTTP_400_BAD_REQUEST)

# Esquema personalizado para documentar a visualização de listagem de taxis no Swagger
listTaxis = taxis_list_schema(method='get')(listTaxis)

# Function to list all trajectories
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
