import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsTrajectories import listTrajectories
from fleet_management_app.models import Trajectories, Taxis
from unittest.mock import patch
from datetime import datetime

@pytest.fixture(scope='module')
def mock_trajectories_queryset(request):
    mock_taxis = [
        Taxis(id=1, plate="ABCD-1234"),
        Taxis(id=2, plate="DEFG-4567")
    ]

    mock_trajectories = [
        Trajectories(id=3, taxi=mock_taxis[0], date=datetime(2024, 5, 10, 5, 10, 2), latitude=10.1234, longitude=20.5678),
        Trajectories(id=4, taxi=mock_taxis[1], date=datetime(2024, 5, 9, 9, 10, 3), latitude=11.4321, longitude=21.8765)
    ]
    with patch('fleet_management_app.views.viewsTrajectories.Trajectories.objects.all') as mock_trajectories_queryset:
        # Crie um mock do queryset de Trajectories
        mock_trajectories_queryset.return_value = mock_trajectories
        yield mock_trajectories_queryset

def test_list_trajectories_endpoint(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/trajectories/')
    response = listTrajectories(request)

    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0

def test_list_trajectories_filter_id(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with filter parameter
    request = factory.get('/api/trajectories/', {'filter_by':1})
    response = listTrajectories(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['taxi']['id'] == 1

def test_list_trajectories_sort_desc(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with sort parameter
    request = factory.get('/api/trajectories/', {'sort_by': '-plate'})
    response = listTrajectories(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['taxi']['plate'] == "DEFG-4567"
    assert response.data['results'][1]['taxi']['plate'] == "ABCD-1234"

def test_list_trajectories_sort_asc(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with sort parameter
    request = factory.get('/api/trajectories/', {'sort_by': 'latitude'})
    response = listTrajectories(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['latitude'] == 10.1234
    assert response.data['results'][1]['latitude'] == 11.4321

def test_list_trajectires_search_plate(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/trajectories/', {'search':'ABCD-1234'})
    response = listTrajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['taxi']['plate'] == 'ABCD-1234'

def test_list_trajectires_search_id(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/trajectories/', {'search':3})
    response = listTrajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['id'] == 3

def test_list_trajectires_search_date(mock_trajectories_queryset):
    factory = APIRequestFactory()
    
    search_date = datetime(2024, 5, 10, 5, 10, 2).isoformat()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/trajectories/', {'search':search_date})
    response = listTrajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['date'] == '2024-05-10T05:10:02Z'

def test_list_trajectories_page_number(mock_trajectories_queryset):
    # Mocking the queryset with more than one page of data
    mock_taxis = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # Creating 20 mock taxis
    mock_trajectories = [
        Trajectories(
            id=i, 
            taxi=mock_taxis[i - 1], 
            date=datetime(i,m,i,i,i,i), 
            latitude=i, 
            longitude=i
            ) 
            for i in range(1, 21) for m in range(1,12)
    ]
    mock_trajectories_queryset.return_value = mock_trajectories

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/trajectories/', {'page': 1})
    response = listTrajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 10  # Assuming page size is set to 10
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 22
    assert response.data['next'] is not None
    assert response.data['previous'] is None

def test_list_trajectories_page_size(mock_trajectories_queryset):
    # Mocking the queryset with more than one page of data
    mock_taxis = [Taxis(id=i, plate=f"ABC-{i}") for i in range(1, 21)]  # Creating 20 mock taxis
    mock_trajectories = [
        Trajectories(
            id=i, 
            taxi=mock_taxis[i - 1], 
            date=datetime(i,m,i,i,i,i), 
            latitude=i, 
            longitude=i
            ) 
            for i in range(1, 21) for m in range(1,12)
    ]
    mock_trajectories_queryset.return_value = mock_trajectories

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/trajectories/', {'page_size': 5})
    response = listTrajectories(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 5  # Assuming page size is set to 5
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 44
    assert response.data['next'] is not None
    assert response.data['previous'] is None

