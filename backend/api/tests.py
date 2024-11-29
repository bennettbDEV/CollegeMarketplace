from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, CoreAPIClient, RequestsClient

from api.models import Listing


# Create your tests here.
class ListingAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()  # Initialize the APIClient
        self.list_url = reverse('listing-list')

        # Create test listing here

    def test_get_listings(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Listing", [item.get("title") for item in response.data.get("results")])