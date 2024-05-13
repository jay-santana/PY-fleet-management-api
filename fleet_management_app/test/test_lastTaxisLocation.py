import pytest
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsLastTaxisLocation import last_taxis_location
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
        Trajectories(id=1, taxi=mock_taxis[0], date=datetime(2024, 5, 10, 6, 30, 15), latitude=12.3456, longitude=23.4567),
        Trajectories(id=3, taxi=mock_taxis[0], date=datetime(2024, 5, 10, 5, 10, 2), latitude=10.1234, longitude=20.5678),
        Trajectories(id=2, taxi=mock_taxis[1], date=datetime(2024, 5, 9, 10, 15, 30), latitude=13.9876, longitude=24.5678),
        Trajectories(id=4, taxi=mock_taxis[1], date=datetime(2024, 5, 9, 9, 10, 3), latitude=11.4321, longitude=21.8765),
    ]
   # Lista para armazenar as últimas localizações de cada táxi
    last_locations = []
    for taxi in mock_taxis:
        # Filtra as trajetórias apenas para o táxi atual
        taxi_trajectories = [t for t in mock_trajectories if t.taxi_id == taxi.id]
        # Encontra a última trajetória com base na data
        last_trajectory = max(taxi_trajectories, key=lambda x: x.date)
        last_locations.append(last_trajectory)

    with patch('fleet_management_app.views.viewsLastTaxisLocation.LastLocationsUtils.get_taxis_last_location') as mock_trajectories_queryset:
        # Crie um mock do queryset de Trajectories
        mock_trajectories_queryset.return_value = last_locations
        yield mock_trajectories_queryset

def test_last_taxis_location_endpoint(mock_trajectories_queryset):
    factory = APIRequestFactory()

    # Making a GET request to the endpoint
    request = factory.get('/api/lastlocation/')
    response = last_taxis_location(request)

    # Asserting that the list of taxis is not empty
    assert response.status_code == 200
    assert len(response.data['results']) > 0

    # Getting the latest trajectory from the results
    assert response.data['results'][0]['date'] == '2024-05-10T06:30:15Z'
    assert response.data['results'][1]['date'] == '2024-05-09T10:15:30Z'
