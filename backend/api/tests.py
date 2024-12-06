# api/tests.py
import os
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
from backend.settings import BASE_DIR


"""
Functions to help setup Tests
"""


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


"""
Create Tests Here
"""


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, "tmp/test_media/"))
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

    def _create_test_listings(self, num_listings=1, base_title="TestListing"):
        # Create test listings here
        test_image = self._generate_test_image()

        for i in range(1, num_listings + 1):
            data = {
                "title": f"{base_title}{i}",
                "description": f"This is test description {i}.",
                "price": f"{i}{i}",
                "image": test_image,
                "tags": ["Test", "Testing", "Development"],
                "condition": "Well Worn",
            }
            response = self.client.post(
                self.list_listings_url, data, format="multipart"
            )
            if response and response.status_code == 201:
                self.listing_ids.append(response.data.get("id"))
            else:
                print(response.data)

    def _delete_test_listings(self):
        for listing_id in self.listing_ids:
            url = reverse("listing-detail", args=[listing_id])
            response = self.client.delete(url)

    # Before
    def setUp(self):
        super().setUp()
        self.listing_handler = ListingHandler()
        self.list_listings_url = reverse("listing-list")
        self.listing_ids = []

    # After
    def tearDown(self):
        self._delete_test_listings()
        super().tearDown()

    def test_authenticated_get_listings(self):
        # Create 1 listing
        listing_title = "TestListing1"
        # Helper method will create 1 listing named TestListing1 based on the given parameters
        self._create_test_listings(1, "TestListing")

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
                listing.get("title") == listing_title
                for listing in response.data.get("results")
            ):
                found_listing = True
                break

            # If no listing found and we have reached the last page, break
            # No "next" link means we are at the last page
            if not response.data.get("links").get("next"):
                break

            page += 1

        # Assert that the listing was found, return string with better description if not
        self.assertTrue(
            found_listing, f"{listing_title} was not found in any of the pages."
        )

    def test_unauthenticated_get_listings(self):
        # Create 1 listing
        listing_title = "TestListing1"
        # Helper method will create 1 listing named TestListing1 based on the given parameters
        self._create_test_listings(1, "TestListing")

        # Stop including any credentials
        self.client.credentials()

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
                listing.get("title") == listing_title
                for listing in response.data.get("results")
            ):
                found_listing = True
                break

            # If no listing found and we have reached the last page, break
            # No "next" link means we are at the last page
            if not response.data.get("links").get("next"):
                break

            page += 1

        # Assert that the listing was found, return string with better description if not
        self.assertTrue(
            found_listing, f"{listing_title} was not found in any of the pages."
        )

    # This method should only be run in development env, never in prod because it deletes all listings
    def _test_empty_listings_response(self):
        # Ensure there are no listings in the database
        # Make method in listinghandler to Delete all listings

        response = self.client.get(self.list_listings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("results", []), [])

    def test_invalid_page_number(self):
        response = self.client.get(f"{self.list_listings_url}?page=999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail"), "Invalid page.")


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
-Chase Test 
-run:
python manage.py test api.tests.LikeListingTestCase.test_like_listing
python manage.py test api.tests.LikeListingTestCase.test_like_nonexistent_listing
python manage.py test api.tests.LikeListingTestCase.test_like_deleted_listing
"""


# TEST: like listing
class LikeListingTestCase(AuthenticatedAPITestCase):
    # Function: setup a test image for a test listing
    def generate_test_image(self):
        img = Image.new(
            "RGB", (100, 100), color=(255, 0, 0)
        )  # Create a 100x100 red image
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", buffer.read(), content_type="image/jpeg"
        )

    # Function: setup data (user and listing)
    def setUp(self):
        """
        Set up the test environment
        """
        super().setUp()
        test_image = self.generate_test_image()

        # create a test listing
        self.test_listing_data = {
            "title": "Test Listing",
            "condition": "New",
            "description": "A sample test listing for testing like functionality.",
            "image": test_image,
            "price": 999.0,
            "likes": 0,
            "dislikes": 0,
            "tags": ["Test", "Sample"],
        }

        # Retrieve the authenticated user's ID
        self.user_id = self.user_handler.get_user_by_username("TestUsername").id

        # Create the listing and retrieve its ID from the response
        response = ListingHandler().create_listing(
            validated_data=self.test_listing_data, user_id=self.user_id
        )

        # Debugging: Print the response data
        # print(f"Create Listing Response: {response.data}")

        # Check that the response is successful and contains the listing ID
        assert response.status_code == 201, f"Failed to create listing: {response.data}"
        self.listing_id = response.data.get("id")
        assert (
            self.listing_id is not None
        ), "Listing ID was not returned in the response."

        # Define the like endpoint for the created listing
        self.like_url = reverse("listing-like-listing", kwargs={"pk": self.listing_id})

    # Function: delete this test data
    def tearDown(self):
        """
        Tear down the test environment by deleting the test listing and cleaning up resources.
        """
        # Check if the listing ID is set
        if self.listing_id:
            # Construct the endpoint for deleting the listing
            url = reverse("listing-detail", args=[self.listing_id])

            # Send a DELETE request using the authenticated client
            response = self.client.delete(url)

        # Call the parent teardown for user cleanup
        super().tearDown()

    """
    Unit Test Cases
    """

    # Case: a normal liking a listing
    def test_like_listing(self):
        # Send a POST request to the like endpoint
        response = self.client.post(self.like_url)

        # Verify the response status is 204 No Content (success)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Expected status 204, got {response.status_code}.",
        )

        # Fetch the updated listing data to verify the like count
        updated_listing = ListingHandler().get_listing(self.listing_id)

        # evaluate
        self.assertEqual(
            updated_listing["likes"],
            1,
            f"Expected 1 like, got {updated_listing['likes']}.",
        )

    # Case: liking a non-existent listing
    def test_like_nonexistent_listing(self):
        invalid_url = reverse("listing-like-listing", kwargs={"pk": -100})
        response = self.client.post(invalid_url)

        # evaluate
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status 404, got {response.status_code}.",
        )

    # Case: liking a listing that has been deleted.
    def test_like_deleted_listing(self):
        # Delete the listing
        url = reverse("listing-detail", args=[self.listing_id])
        self.client.delete(url)

        # Try liking the deleted listing
        response = self.client.post(self.like_url)

        # evaluate
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status 404, got {response.status_code}.",
        )


"""
TEST CLASS: x
-Chase Test 2
-run:
"""


# TEST: x
class x(AuthenticatedAPITestCase):
    """
    Test case for x
    """

    # Function: setup data
    def setUp(self):
        """
        Set up the test environment by creating a test listing.
        """
        super().setUp()

    # Function: delete this test data
    def tearDown(self):
        """
        Tear down the test environment by deleting the test listing and cleaning up resources.
        """
        # Call the parent teardown for user cleanup
        super().tearDown()
"""
TEST CLASS: Dislike Listing Testcase
-Trevin Test Case 1
-run:
python manage.py test api.tests.DislikeListingTestCase
"""
class DislikeListingTestCase(AuthenticatedAPITestCase):
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
    #setup function
    def setUp(self):
        #setup user using super class function
        super().setUp()
        test_image = self._generate_test_image()
        # create a test listing
        self.test_listing_data = {
            "title": "Test Listing",
            "condition": "New",
            "description": "A sample test listing for testing functionality.",
            "image": test_image,
            "price": 999.0,
            "likes": 0,
            "dislikes": 0,
            "tags": ["Test", "Sample"],
        }
        # Retrieve the authenticated user's ID
        self.user_id = self.user_handler.get_user_by_username("TestUsername").id
        # Create the listing and retrieve its ID from the response
        response = ListingHandler().create_listing(
            validated_data=self.test_listing_data, user_id=self.user_id
        )
        #check that the response is successful and contains the listing ID
        assert response.status_code == 201, f"Failed to create listing: {response.data}"
        self.listing_id = response.data.get("id")
        assert (
            self.listing_id is not None
        ), "Listing ID was not returned in the response."
        #define the dislike endpoint for the created listing
        self.dislike_url = reverse("listing-dislike-listing", kwargs={"pk": self.listing_id})
        #we all good
        
    
    def test_dislike_listing(self):
        # Send a POST request to the dislike endpoint
        response = self.client.post(self.dislike_url)
        # Verify the response status is 204 No Content (success)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Expected status 204, got {response.status_code}.",
        )
        # Fetch the updated listing data to verify the like count
        updated_listing = ListingHandler().get_listing(self.listing_id)
        # evaluate
        self.assertEqual(
            updated_listing["dislikes"],
            1,
            f"Expected 1 like, got {updated_listing['dislikes']}.",
        )
    def test_dislike_nonexistent_listing(self):
        invalid_url = reverse("listing-dislike-listing", kwargs={"pk": -21417926535879})
        response = self.client.post(invalid_url)
        # evaluate
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status 404, got {response.status_code}.",
        )
    #teardown function
    def tearDown(self):
        #clean up after testing
        # Check if the listing ID is set
        if self.listing_id:
            # Construct the endpoint for deleting the listing
            url = reverse("listing-detail", args=[self.listing_id])
            # Send a DELETE request using the authenticated client
            response = self.client.delete(url)
        super().tearDown()
"""
TEST CLASS: Dislike Listing Testcase
-Trevin Test Case 1
-run:
python manage.py test api.tests.DislikeListingTestCase
"""
class RetrieveListingTestCase(AuthenticatedAPITestCase):
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
    #setup function
    def setUp(self):
        #setup user using super class function
        super().setUp()
        test_image = self._generate_test_image()
        # create a test listing
        self.test_listing_data = {
            "title": "Test Listing",
            "condition": "New",
            "description": "A sample test listing for testing functionality.",
            "image": test_image,
            "price": 999.0,
            "likes": 0,
            "dislikes": 0,
            "tags": ["Test", "Sample"],
        }
        # Retrieve the authenticated user's ID
        self.user_id = self.user_handler.get_user_by_username("TestUsername").id
        # Create the listing and retrieve its ID from the response
        response = ListingHandler().create_listing(
            validated_data=self.test_listing_data, user_id=self.user_id
        )
        #check that the response is successful and contains the listing ID
        assert response.status_code == 201, f"Failed to create listing: {response.data}"
        self.listing_id = response.data.get("id")
        assert (
            self.listing_id is not None
        ), "Listing ID was not returned in the response."
        #define the dislike endpoint for the created listing
        self.dislike_url = reverse("listing-dislike-listing", kwargs={"pk": self.listing_id})
        #we all good
        
    
    def test_retrieve_listing(self):
        # Send a POST request to the dislike endpoint
        response = self.client.post(self.dislike_url)
        # Verify the response status is 204 No Content (success)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Expected status 204, got {response.status_code}.",
        )
        # Fetch the updated listing data to verify the like count
        updated_listing = ListingHandler().get_listing(self.listing_id)
        # evaluate
        self.assertEqual(
            updated_listing["dislikes"],
            1,
            f"Expected 1 like, got {updated_listing['dislikes']}.",
        )
    def test_dislike_nonexistent_listing(self):
        invalid_url = reverse("listing-dislike-listing", kwargs={"pk": -21417926535879})
        response = self.client.post(invalid_url)
        # evaluate
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status 404, got {response.status_code}.",
        )
    #teardown function
    def tearDown(self):
        #clean up after testing
        # Check if the listing ID is set
        if self.listing_id:
            # Construct the endpoint for deleting the listing
            url = reverse("listing-detail", args=[self.listing_id])
            # Send a DELETE request using the authenticated client
            response = self.client.delete(url)
        super().tearDown()