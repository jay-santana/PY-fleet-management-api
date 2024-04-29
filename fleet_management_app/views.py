from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Max

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework import status

from .models import Taxis, Trajectories
from .serializers import TaxisSerializer, TrajectoriesSerializer
from .schemas import taxis_list_schema, trajectories_list_schema, last_taxi_location_schema
from .utils import TaxiUtils, TrajectoriesUtils, LastLocationsUtils

import json

# Create your views here.

# Function to list all taxis
@api_view(['GET'])
def listTaxis(request):
    """
    List all taxis with optional filtering, sorting, searching, and pagination.
    """
    if request.method == 'GET':
        # Instantiate TaxiUtils class with the request object
        taxi_utils = TaxiUtils(request)
        # Get request query parameters
        filter_by = request.query_params.get('filter_by')
        sort_by = request.query_params.get('sort_by')
        search = request.query_params.get('search')

        # Get page size and page number
        page_size = taxi_utils.get_page_size()
        page_number = taxi_utils.get_page_number()

        # Filter, sort, and search taxis
        taxis = Taxis.objects.all()
        taxis = taxi_utils.filter_taxis(taxis, filter_by)
        taxis = taxi_utils.sort_taxis(taxis, sort_by)
        taxis = taxi_utils.search_taxis(taxis, search)
        
        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(taxis, request)

        # Verificar se a lista de táxis está vazia
        if not result_page:
            return Response({'detail': 'Nenhum táxi encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
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
    """
    List all trajectories with optional filtering, sorting, searching, and pagination.
    """
    if request.method == 'GET':
        # Instantiate TrajectoriesUtils class with the request object
        trajectories_utils = TrajectoriesUtils(request)
        # Get request query parameters
        filter_by = request.query_params.get('filter_by')
        sort_by = request.query_params.get('sort_by')
        search = request.query_params.get('search')

        # Get page size and page number
        page_size = trajectories_utils.get_page_size()
        page_number = trajectories_utils.get_page_number()

        # Filter, sort, and search taxis
        trajectories = Trajectories.objects.all()
        trajectories = trajectories_utils.filter_trajectories(trajectories, filter_by)
        trajectories = trajectories_utils.sort_trajectories(trajectories, sort_by)
        trajectories = trajectories_utils.search_trajectories(trajectories, search)
       
        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(trajectories, request)
        
        # Verificar se a lista de táxis está vazia
        if not result_page:
            return Response({'detail': 'Nenhum táxi encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the paginated queryset
        serializer = TrajectoriesSerializer(result_page, many=True)
        
        # Construct response data
        response = paginator.get_paginated_response(serializer.data)
        
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
         # Add current_page and total_pages
        response.data = {**pagination_info, **response.data}
        
        return response   # Return the serialized data 
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Esquema personalizado para documentar a visualização de listagem de trajetórias no Swagger
listTrajectories = trajectories_list_schema(method='get')(listTrajectories)

# Function to list the last location of all taxis
@api_view(['GET'])
def last_taxi_locations(request):
    """
    Get the last location of each taxi with optional filtering, sorting, searching, and pagination.
    """
    if request.method == 'GET':
        # Instantiate LastLocationsUtils class with the request object
        last_locations_utils = LastLocationsUtils(request)
        
        # Get request query parameters
        filter_by = request.query_params.get('filter_by')
        sort_by = request.query_params.get('sort_by')
        search = request.query_params.get('search')
        
        # Get page size and page number
        page_size = last_locations_utils.get_page_size()
        page_number = last_locations_utils.get_page_number()

        # Get the latest locations of all taxis
        last_trajectories = last_locations_utils.get_last_taxi_locations()

        # Check if the list of taxis is empty
        if not last_trajectories:
            return Response({'detail': 'Nenhum táxi encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Filter, sort and search trajectories
        last_trajectories = last_locations_utils.filter_last_locations(last_trajectories, filter_by)
        last_trajectories = last_locations_utils.sort_last_locations(last_trajectories, sort_by)
        last_trajectories = last_locations_utils.search_last_locations(last_trajectories, search)  
        
        # Paginate the queryset using PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(last_trajectories, request)
        
        # Serialize the paginated queryset
        serializer = TrajectoriesSerializer(result_page, many=True)

        # Construct response data
        response = paginator.get_paginated_response(serializer.data)
    
        # Including additional pagination information at the beginning of the response object
        pagination_info = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages
        }
        # Add current_page and total_pages
        response.data = {**pagination_info, **response.data}
    
        return response   # Return the serialized data 

    return Response({'detail': 'Por favor, forneça um taxi_id válido'}, status=status.HTTP_400_BAD_REQUEST)

# Esquema personalizado para documentar a visualização de última localização do táxi no Swagger
last_taxi_locations = last_taxi_location_schema(method='get')(last_taxi_locations)



# def databaseEmDjango():
# data = User.objects.get(pk='gabriel_nick')          # OBJETO
# data = User.objects.filter(user_age='25')           # QUERYSET
# data = User.objects.exclude(user_age='25')          # QUERYSET
# data.save()
# data.delete()
