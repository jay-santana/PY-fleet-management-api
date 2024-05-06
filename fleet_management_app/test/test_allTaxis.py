from django.test import TestCase
from rest_framework.test import APIRequestFactory
from fleet_management_app.views.viewsTaxis import listTaxis
from ..models import Taxis
from unittest.mock import patch

class TaxisEndpointTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('fleet_management_app.views.viewsTaxis.Taxis.objects.all')
    def test_list_taxis_endpoint(self, mock_taxis_queryset):
        # Mocking the queryset
        mock_taxis = [
            Taxis(id=1, plate="ABCD-1234"),
            Taxis(id=2, plate="DEFG-4567")
        ]
        mock_taxis_queryset.return_value = mock_taxis

        # Making a GET request to the endpoint
        request = self.factory.get('http://localhost:8000/api/taxis/')
        response = listTaxis(request)

        # Asserting the response status code
        self.assertEqual(response.status_code, 200)

        # Asserting the response data
        expected_data = {
            'count': len(mock_taxis),
            'current_page': 1,
            'next': None,
            'previous': None,
            'total_pages': 1,
            'results': [
                {'id': taxi.id, 'plate': taxi.plate} for taxi in mock_taxis
            ]
        }
        self.assertEqual(response.data, expected_data)

