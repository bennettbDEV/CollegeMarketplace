#api/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, CoreAPIClient, RequestsClient
from api.models import Listing
from api.handlers import ListingHandler
from django.contrib.auth.models import User
from unittest.mock import patch



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



'''
TEST CLASS: LikeListingTestCase
-Chase Test 1
-run: python manage.py test api.tests.LikeListingTestCase.test_like_listing
'''
#TEST: like listing
class LikeListingTestCase(APITestCase):
    """
    Test class for testing the like functionality of a listing.
    """

    def setUp(self):
        """
        Set up a test listing and initialize the like endpoint.
        """
        # Create a test listing using the handler
        self.test_listing = {
            "title": "Test Listing",
            "condition": "New",
            "description": "A sample test listing",
            "price": 999.0,
            "likes": 0,
            "dislikes": 0,
        }
        self.user_id = 29  #Replace with a valid user ID if needed

        # Create the listing
        ListingHandler().create_listing(validated_data=self.test_listing, user_id=self.user_id)

        # Define the like endpoint
        self.like_url = reverse("listing-like-listing", kwargs={"pk": 1})

    def test_like_listing(self):
        """
        Test liking a listing and incrementing the like count.
        """
        # Send a POST request to like the listing
        response = self.client.post(self.like_url)

        # Assert the response status is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Retrieve the updated listing
        updated_listing = ListingHandler().get_listing(1)

        # Assert the like count has incremented by 1
        self.assertEqual(updated_listing["likes"], 1)
