import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsLastTaxisLocation import lastTaxisLocation
from fleet_management_app.models import Trajectories, Taxis
from unittest.mock import patch
from datetime import datetime

@pytest.fixture(scope='module')
def mock_last_taxis_location_queryset(request):
    mock_taxis = [
        Taxis(id=1, plate="ABCD-1234"),
        Taxis(id=2, plate="DEFG-4567")
    ]

    mock_trajectories = [
        Trajectories(id=3, taxi=mock_taxis[0], date=datetime(2024, 5, 10, 6, 30, 15), latitude=12.3456, longitude=23.4567),
        Trajectories(id=4, taxi=mock_taxis[0], date=datetime(2024, 5, 10, 5, 10, 2), latitude=10.1234, longitude=20.5678),
        Trajectories(id=5, taxi=mock_taxis[1], date=datetime(2024, 5, 9, 10, 15, 30), latitude=13.9876, longitude=24.5678),
        Trajectories(id=6, taxi=mock_taxis[1], date=datetime(2024, 5, 9, 9, 10, 3), latitude=11.4321, longitude=21.8765),
    ]

    # Lista para armazenar as últimas localizações de cada táxi
    last_locations = []
    for taxi_id in [taxi.id for taxi in mock_taxis]:
        # Filtra as trajetórias apenas para o táxi atual
        taxi_trajectories = [t for t in mock_trajectories if t.taxi.id == taxi_id]
        if taxi_trajectories:
            # Encontra a última trajetória com base na data
            last_trajectory = max(taxi_trajectories, key=lambda x: x.date)
            last_locations.append(last_trajectory)

    with patch('fleet_management_app.views.viewsLastTaxisLocation.LastTaxisLocationUtils.get_taxis_last_location') as mock_last_taxis_location_queryset:
        # Crie um mock do queryset de Trajectories
        mock_last_taxis_location_queryset.return_value = last_locations
        yield mock_last_taxis_location_queryset

def test_last_taxis_location_endpoint(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/lastlocation/')
    response = lastTaxisLocation(request)
    
    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0

    # Getting the latest trajectory from the results
    assert response.data['results'][0]['date'] == '2024-05-10T06:30:15Z'
    assert response.data['results'][1]['date'] == '2024-05-09T10:15:30Z'

def test_last_taxis_location_filter_id(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with filter parameter
    request = factory.get('/api/lastlocation/', {'filter_by':1})
    response = lastTaxisLocation(request)

    # Asserting the response data
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['taxi']['id'] == 1

def test_last_taxis_location_sort_id_asc(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Fazendo a requisição com o parâmetro de ordenação ascendente pelo ID
    request = factory.get('/api/lastlocation/', {'sort_by': 'id'})
    response = lastTaxisLocation(request)

    # Verificando a ordenação dos resultados
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    
    # Verificando se os IDs estão ordenados em ordem ascendente
    assert response.data['results'][0]['taxi']['id'] == 1
    assert response.data['results'][1]['taxi']['id'] == 2

def test_last_taxis_location_sort_plate_desc(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Fazendo a requisição com o parâmetro de ordenação ascendente pelo ID
    request = factory.get('/api/lastlocation/', {'sort_by': '-plate'})
    response = lastTaxisLocation(request)

    # Verificando a ordenação dos resultados
    assert response.status_code == 200
    assert len(response.data['results']) == 2
    
    # Verificando se os IDs estão ordenados em ordem ascendente
    assert response.data['results'][0]['taxi']['plate'] == "DEFG-4567"
    assert response.data['results'][1]['taxi']['plate'] == "ABCD-1234"
    
def test__last_taxis_location_sort_search_plate(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/lastlocation/', {'search':'ABCD-1234'})
    response = lastTaxisLocation(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['taxi']['plate'] == 'ABCD-1234'

def test__last_taxis_location_sort_search_long(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/lastlocation/', {'search': 23.4567})
    response = lastTaxisLocation(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert 'results' in response.data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['longitude'] == 23.4567

def test__last_taxis_location_sort_search_date(mock_last_taxis_location_queryset):
    factory = APIRequestFactory()

    search_date = datetime(2024, 5, 9, 10, 15, 30).isoformat()

    # Making a GET request to the endpoint with search parameter
    request = factory.get('/api/lastlocation/', {'search': search_date})
    response = lastTaxisLocation(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['date'] == '2024-05-09T10:15:30Z'

def test_last_taxis_location_page_number(mock_last_taxis_location_queryset):
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
    mock_last_taxis_location_queryset.return_value = mock_trajectories

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/lastlocation/', {'page': 1})
    response = lastTaxisLocation(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 10  # Assuming page size is set to 10
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 22
    assert response.data['next'] is not None
    assert response.data['previous'] is None

def test_last_taxis_location_page_size(mock_last_taxis_location_queryset):
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
    mock_last_taxis_location_queryset.return_value = mock_trajectories

    factory = APIRequestFactory()

    # Making a GET request to the endpoint with page parameter
    request = factory.get('/api/lastlocation/', {'page_size': 5})
    response = lastTaxisLocation(request)

    # Asserting the response status code
    assert response.status_code == 200

    # Asserting the response data
    assert len(response.data['results']) == 5  # Assuming page size is set to 5
    assert response.data['current_page'] == 1
    assert response.data['total_pages'] == 44
    assert response.data['next'] is not None
    assert response.data['previous'] is None

