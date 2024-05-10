import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsTaxis import listTaxis
from fleet_management_app.models import Taxis
from unittest.mock import patch

@pytest.fixture(scope='module')
def mock_taxis_queryset(request):
    mock_taxis = [
        Taxis(id=1, plate="ABCD-1234"),
        Taxis(id=2, plate="DEFG-4567")
    ]
    with patch('fleet_management_app.views.viewsTaxis.Taxis.objects.all') as mock_taxis_queryset:
        mock_taxis_queryset.return_value = mock_taxis
        yield mock_taxis_queryset

def test_list_taxis_endpoint(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/taxis/')
    response = listTaxis(request)

    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0

def test_list_taxis_filter_id(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with filter parameter
    request = factory.get('/api/taxis/', {'id': '1'})
    response = listTaxis(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['id'] == 1

def test_list_taxis_filter_plate(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with filter parameter
    request = factory.get('/api/taxis/', {'plate': 'ABCD-1234'})
    response = listTaxis(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['plate'] == 'ABCD-1234'

def test_list_taxis_sort_id(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with sort parameter
    request = factory.get('/api/taxis/', {'order_by': '-id'})
    response = listTaxis(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][1]['id'] == 2
    assert response.data['results'][0]['id'] == 1

def test_list_taxis_sort_plate(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with sort parameter
    request = factory.get('/api/taxis/', {'order_by': '-plate'})
    response = listTaxis(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][1]['plate'] == "DEFG-4567"
    assert response.data['results'][0]['plate'] == 'ABCD-1234'

def test_list_taxis_search_id(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/taxis/', {'id': '2'})
    response = listTaxis(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 2
    assert response.data['results'][1]['id'] == 2

def test_list_taxis_search_plate(mock_taxis_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/taxis/', {'plate': 'ABCD'})
    response = listTaxis(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['plate'] == 'ABCD-1234'

def test_list_taxis_page_size(mock_taxis_queryset):
    # Mocking the queryset with more than one page of data
    mock_taxis = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # Creating 20 mock taxis
    mock_taxis_queryset.return_value = mock_taxis

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/taxis/', {'page_size': 1})
    response = listTaxis(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1  # Assuming page size is set to 1
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 20
    assert response.data['next'] is not None
    assert response.data['previous'] is None

def test_list_taxis_page_number(mock_taxis_queryset):
    # Mocking the queryset with more than one page of data
    mock_taxis = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # Creating 20 mock taxis
    mock_taxis_queryset.return_value = mock_taxis

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/taxis/', {'page': 2})
    response = listTaxis(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 10  # Assuming page size is set to 10
    assert response.data['current_page'] == 2
    assert response.data['total_pages'] == 2
    assert response.data['next'] is None
    assert response.data['previous'] is not None

