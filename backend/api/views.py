#api/views.py
'''
CLASSES: 
LoginView, StandardResultsSetPagination, UserViewSet, ListingViewSet, 
ServeImageView, 
'''

import mimetypes
import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .handlers import ListingHandler, UserHandler
from .models import Listing, User
from .serializers import ListingSerializer, LoginSerializer, UserSerializer

'''
CLASS: LoginView
'''
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_handler = UserHandler()

    # Login request
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # If valid credentials
        if serializer.is_valid():
            user_data = serializer.validated_data
            response = self.user_handler.login(user_data)
            return response

        # If the serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
CLASS: StandardResultsSetPagination
'''
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )


'''
CLASS: UserViewSet
'''
class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_handler = UserHandler()

    def get_permissions(self):
        # User must be authenticated if performing any action other than create/retrieve
        self.permission_classes = ([AllowAny] if (self.action in ["create", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        # Gets all users
        users = self.user_handler.list_users()
        return users

    # Crud actions
    def list(self, request):
        """Lists all user objects.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: An object containing a list of all user objects.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # Fallback if pagination is not applicable
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Creates a new User.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: If request data is valid, the DRF Response object will contain authentication tokens.
            Response will always include an HTTP status.
        """

        # Serialize/Validate data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            response = self.user_handler.register_user(validated_data)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieves the User with the specified id.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the User. Defaults to None.

        Returns:
            Response: A DRF Response object with the user's data, if the user exists.
            Response will always include an HTTP status.
        """

        user = self.user_handler.get_user(pk)
        if user:
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "User with that id not found."}, status=status.HTTP_404_NOT_FOUND,)

    def partial_update(self, request, pk=None):
        """Updates the specified user with the given data.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the User. Defaults to None.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """

        try:
            response = self.user_handler.partial_update_user(request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

    def destroy(self, request, pk=None):
        """Deletes the specified User.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the User. Defaults to None.

        Returns:
            Resposne: A DRF Response object with an HTTP status.
        """
        try:
            response = self.user_handler.delete_user(request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    '''
    Block/Unblock Content 
    '''
    #Function: block
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def block_user(self, request, pk=None):
        """
        Blocks the specified user.

        Args:
            request (Request): DRF request object.
            pk (int): The ID of the user to be blocked.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            blocker_id = request.user.id
            blocked_id = int(pk)

            # Call the handler method to block the user
            response = self.user_handler.block_user(blocker_id, blocked_id)
            return response

        except ValueError:
            return Response(
                {"error": "Invalid user ID."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error blocking user: {e}")
            return Response({"error": "An unexpected error occurred while blocking the user."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Function: unblock
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unblock_user(self, request, pk=None):
        """
        Unblocks the specified user.

        Args:
            request (Request): DRF request object.
            pk (int): The ID of the user to be unblocked.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            blocker_id = request.user.id
            blocked_id = int(pk)

            # Call the handler method to unblock the user
            response = self.user_handler.unblock_user(blocker_id, blocked_id)
            return response
        
        #if error
        except ValueError:
            return Response({"error": "Invalid user ID."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error unblocking user: {e}")
            return Response({"error": "An unexpected error occurred while unblocking the user."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #Function: check if a user is blocked
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def is_user_blocked(self, request, pk=None):
        """
        Checks if the authenticated user has been blocked by the specified user.

        Args:
            request (Request): DRF request object.
            pk (int): The ID of the user to check against.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            sender_id = request.user.id
            receiver_id = int(pk)

            # Call the handler method to check if the user is blocked
            response = self.user_handler.is_user_blocked(sender_id, receiver_id)
            return response
        
        #if error
        except ValueError:
            return Response({"error": "Invalid user ID."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error checking block status: {e}")
            return Response({"error": "An unexpected error occurred while checking block status."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
CLASS: ListingViewSet
'''
# Listing controller/handler
class ListingViewSet(viewsets.GenericViewSet):
    serializer_class = ListingSerializer
    pagination_class = StandardResultsSetPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing_handler = ListingHandler()

    def get_permissions(self):
        # User must be authenticated if performing any action other than retrieve/list
        self.permission_classes = ([AllowAny] if (self.action in ["list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        filters = {} # No filters by default

        search_term = self.request.query_params.get("search", None)
        ordering = self.request.query_params.get("ordering", None)
        
        # Add supported filters
        for param, value in self.request.query_params.items():
            if param in ["min_price", "max_price", "min_likes", "max_dislikes", "condition"]:  # Allowed filters
                filters[param] = value

        # Get the filtered and sorted listings
        listings = self.listing_handler.list_filtered_listings(filters, search_term, ordering)

        # Return listings as Listing instances
        return [Listing(**listing) for listing in listings]

    '''
    CRUD actions for ListingViewSet
    '''
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        # Fallback if pagination is not applicable
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id

            response = self.listing_handler.create_listing(serializer.validated_data, user_id)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        print(pk)
        listing = self.listing_handler.get_listing(pk)
        print(listing)
        listing = Listing(**listing)
        if listing:
            serializer = self.get_serializer(listing)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Listing with that id not found."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            response = self.listing_handler.partial_update_listing(request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            response = self.listing_handler.delete_listing(request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    '''
    Favorite/Save Listing actions

    -Router will automatically create a url based on the method name and details in the @action line
    -The url for this method will be listings/{pk}/favorite_listing/
    '''

    #Function: add listing to favorites 
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite_listing(self, request, pk=None):
        """
        Adds a listing to the user's saved/favorite listings list.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the Listing. Defaults to None.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            user_id = request.user.id
            response = self.listing_handler.add_favorite_listing(user_id, pk)
            return response
        except Exception as e:
            print(e)
            return Response({"ERROR: unexpected error while adding the listing to favorites"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #Function: remove listing from favorites 
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_favorite_listing(self, request, pk=None):
        """Removes a listing from the user's saved/favorite listings list.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the Listing. Defaults to None.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            user_id = request.user.id
            response = self.listing_handler.remove_favorite_listing(user_id, pk)
            return response
        except Exception as e:
            print(e)
            return Response({"ERROR: unexpected error while removing the listing from favorites"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    #Function: lists all the listings that have been 'favorited' by the user 
    @action(detail=False, permission_classes=[IsAuthenticated])
    def list_favorite_listings(self, request):
        """
        Fetches all the user's saved/favorite listings.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            user_id = request.user.id
            #Call the handler function to retrieve favorite listings
            response = self.listing_handler.list_favorite_listings(user_id)
            #Return the list of favorite listings
            return response
        except Exception as e:
            # Log the error for debugging
            print(f"Error in list_favorite_listings: {e}")
            # Return a generic server error response
            return Response(
                {"error": "An unexpected error occurred while fetching favorite listings."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    '''
    Like/Dislike actions
    '''

    #Function: "likes" the listing
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like_listing(self, request, pk=None):
        listing = self.listing_handler.get_listing(pk)
        print(type(listing))
        if listing:
            response = self.listing_handler.like_listing(pk, listing["likes"])
            return response
        return Response({"error": "Listing with that id not found."}, status=status.HTTP_404_NOT_FOUND)

    #Function: "dislikes" the listing
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dislike_listing(self, request, pk=None):
        listing = self.listing_handler.get_listing(pk)
        if listing:
            response = self.listing_handler.dislike_listing(pk, listing["dislikes"])
            return response
        return Response({"error": "Listing with that id not found."}, status=status.HTTP_404_NOT_FOUND)


'''
CLASS: ServeImageView
'''
class ServeImageView(View):
    """
    Serve images with correct Content type.
    """
    def get(self, request, image_path):
        # Construct the full path to the image
        full_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, image_path))
        if not full_path.startswith(settings.MEDIA_ROOT):
            return Response({"error": "Invalid image path."}, status=status.HTTP_400_BAD_REQUEST)
        if not os.path.exists(full_path):
            return Response({"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND)

        # Attempt to determine mime type using Mimetypes
        mime_type, _ = mimetypes.guess_type(full_path)
        mime_type = mime_type or "application/octet-stream"

        # Return file with the guessed Content type
        return FileResponse(open(full_path, "rb"), content_type=mime_type)


'''
Non-class Related Functions 
'''
# Function to return to the generate the homepage
def to_backend(request):
    return render(request, 'api/backend.html')