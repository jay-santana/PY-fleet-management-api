from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def base_list_schema(operation_summary, operation_description, item_schema, custom_description, method='get'):
    return swagger_auto_schema(
        method=method,
        manual_parameters=[
            openapi.Parameter('page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page number'),
            openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='page size'),
            openapi.Parameter('sort_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Sort by field'),
            openapi.Parameter('filter_by', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Filter by field'),
            openapi.Parameter('search', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search term'),
        ],
        responses={
            200: openapi.Response(
               description=custom_description,
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=item_schema
                        ),
                    }
                )
            ),
            400: "Bad request",
            404: "Not found",
        },
        operation_summary=operation_summary,
        operation_description=operation_description
    )

def taxis_list_schema(method='get'):
    return base_list_schema(
        operation_summary="Get taxis",
        operation_description="Get a list of all taxis.",
        item_schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'plate': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        custom_description="List of all taxis",
        method=method
    )

def trajectories_list_schema(method='get'):
    return base_list_schema(
        operation_summary="Get trajectories",
        operation_description="Get a list of all trajectories.",
        item_schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'taxi': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'plate': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            }
        ),
        custom_description="List of all trajectories",
        method=method
    )

def last_taxis_location_schema(method='get'):
    return base_list_schema(
        operation_summary="Get last location of each taxi",
        operation_description="Get the last location of each taxi.",
        item_schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'taxi': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'plate': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            }
        ),
        custom_description="List of last location of each taxi",
        method=method
    )


