from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework import status

from ..models import Taxis
from ..serializers import TaxisSerializer
from ..schemas import taxis_list_schema
from ..utils import TaxiUtils

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
