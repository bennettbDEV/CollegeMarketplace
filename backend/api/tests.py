# api/tests.py
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, CoreAPIClient, RequestsClient

from api.handlers import ListingHandler, UserHandler
from api.models import Listing
from api.serializers import ListingSerializer, LoginSerializer, UserSerializer


class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.user_handler = UserHandler()

        data = {
            "username": "TestUsername",
            "password": "TestPassword",
        }
        serializer = UserSerializer(data=data)
        response = None

        # Create test user
        if serializer.is_valid():
            response = self.user_handler.register_user(serializer.validated_data)
        else:
            print(serializer.errors)
            return

        # If test user exists for some reason, login instead
        if response.data.get("error") == "Username already exists.":
            login_serializer = LoginSerializer(
                data={"username": data["username"], "password": data["password"]}
            )

            if login_serializer.is_valid():
                response = self.user_handler.login(
                    user_data=login_serializer.validated_data
                )
            else:
                print(serializer.errors)
                return

        access_token = response.data["access"]
        status_code = response.status_code

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def tearDown(self):
        user = self.user_handler.get_user_by_username("TestUsername")
        url = reverse("user-detail", args=[user.id])
        response = self.client.delete(url)


# Create your tests here.
@override_settings(MEDIA_ROOT="/tmp/test_media/")
class ListListingsAPITestCase(AuthenticatedAPITestCase):
    def _generate_test_image(self):
        img = Image.new(
            "RGB", (100, 100), color=(255, 0, 0)
        )  # Create a 100x100 red image
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", buffer.read(), content_type="image/jpeg"
        )

    def setUp(self):
        super().setUp()
        self.listing_handler = ListingHandler()
        self.list_listings_url = reverse("listing-list")
        self.listing1_id = None

        # Create test listings here
        test_image = self._generate_test_image()

        data = {
            "title": "TestListingOne",
            "description": "This is a test description.",
            "price": "999.99",
            "image": test_image,
            "tags": ["Test", "Testing", "Development"],
            "condition": "Well Worn",
        }
        # serializer = ListingSerializer(data=data)
        response = None

        # if serializer.is_valid():
        response = self.client.post(self.list_listings_url, data, format="multipart")
        if response.status_code == 201:
            self.listing1_id = response.data.get("id")
        else:
            print(response.data)

    def tearDown(self):
        url = reverse("listing-detail", args=[self.listing1_id])
        response = self.client.delete(url)
        super().tearDown()

    def test_get_listings(self):
        found_listing = False
        page = 1
        max_pages = 100

        while page <= max_pages:
            # Construct the URL for the current page
            url = f"{self.list_listings_url}?page={page}"

            # Send GET request for current page
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Check if the listing on the current page
            if any(
                item.get("title") == "TestListingOne"
                for item in response.data.get("results")
            ):
                found_listing = True
                break

            # If no listing found and we have reached the last page, break
            # No "next" link means we are at the last page
            if not response.data.get("links").get("next"):
                break

            page += 1

        # Assert that the listing was found
        self.assertTrue(
            found_listing, "TestListingOne was not found in any of the pages."
        )


class ListingSerializerTestCase(TestCase):
    def test_valid_data(self):
        data = {
            "title": "Valid Listing",
            "description": "This is a valid test listing",
            "price": 20.00,
        }
        serializer = ListingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Valid Listing")

    def test_invalid_data(self):
        data = {
            "description": "Missing title",
            "price": -10.00,  # Invalid price
        }
        serializer = ListingSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("price", serializer.errors)


"""
TEST CLASS: LikeListingTestCase
-Chase Test 1
-run: python manage.py test api.tests.LikeListingTestCase.test_like_listing
"""


# TEST: like listing
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
        self.user_id = 29  # Replace with a valid user ID if needed

        # Create the listing
        ListingHandler().create_listing(
            validated_data=self.test_listing, user_id=self.user_id
        )

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


#Jake test case: Create Listing
class CreateListingTest(AuthenticatedAPITestCase):
    def setup(self):
        super.setup()
        test_img = self._generate_test_image()
        self.test_listing = {
            "title": "Test Listing",
            "condition": "Factory New",
            "description": "A sample test listing",
            "price": 999.0,
            "image": test_img,
            "tags" : ["English", "Writing"]
        }

    def test_create_valid_listing(self):
        url = "listings/"
        response = self.client.post(url, data = self.test_listing, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key,value in self.test_listing.items():
            self.assertEqual(response.data.get(key), value)
        
    def test_create_invalid_listing_title_value():
        url = "listings/"
        

    
    def _generate_test_image(self):
        img = Image.new(
            "RGB", (100, 100), color=(255, 0, 0)
        )  # Create a 100x100 red image
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", buffer.read(), content_type="image/jpeg"
        )
