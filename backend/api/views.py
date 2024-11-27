# api/views.py
import mimetypes
import os

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
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

    # Login request
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # If valid credentials
        if serializer.is_valid():
            user_data = serializer.validated_data
            response = UserHandler.login(UserHandler, user_data)
            return response

        # If the serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
CLASS: UserViewSet
'''
class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_handler = UserHandler()

    def get_permissions(self):
        # User must be authenticated if performing any action other than create/list/retrieve
        self.permission_classes = ([AllowAny] if (self.action in ["create", "list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        # Gets all users
        users = self.user_handler.list_users()
        # ** operator is used to pass all key value pairs to the calling function
        return [User(**user) for user in users]

    # Crud actions
    def list(self, request):
        """Lists all user objects.

        Args:
            request (Request): DRF request object.

        Returns:
            Response: An object containing a list of all user objects.
        """
        users = self.user_handler.list_users()
        # Serialize data for all users -> format data as json
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    # User registration
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
CLASS: ListingViewSet
'''
# Listing controller/handler
class ListingViewSet(viewsets.GenericViewSet):
    serializer_class = ListingSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing_handler = ListingHandler()

    def get_permissions(self):
        # User must be authenticated if performing any action other than retrieve/list
        self.permission_classes = ([AllowAny] if (self.action in ["list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        # Gets all listings -> could be modified later to be filtered
        listings = self.listing_handler.list_listings()
        return [Listing(**listing) for listing in listings]

    '''
    CRUD actions for ListingViewSet
    '''
    def list(self, request):
        listings = self.listing_handler.list_listings()
        serializer = self.get_serializer(listings, many=True)
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
        listing = self.listing_handler.get_listing(pk)
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
            response_data, status_code = self.listing_handler.add_favorite_listing(user_id, pk)
            return Response(response_data, status=status_code)
        except Exception as e:
            return Response({"ERROR: unexpected error while adding the listing to favorites"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #Function: remove listing from favorites 
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
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
            response_data, status_code = self.listing_handler.remove_favorite_listing(user_id, pk)
            return Response(response_data, status=status_code)
        except Exception as e:
            return Response({"ERROR: unexpected error while removing the listing from favorites"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # response = self.listing_handler.remove_favorite_listing(ListingHandler, user_id, listing_id)
        

    # Maybe add to UserViewSet instead?
    # Default method is "get"

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
            favorite_listings = self.listing_handler.list_favorite_listings(user_id)
            #Return the list of favorite listings
            return Response({"favorites": favorite_listings},status=status.HTTP_200_OK)
        except Exception as e:
            # Log the error for debugging
            print(f"Error in list_favorite_listings: {e}")
            # Return a generic server error response
            return Response(
                {"error": "An unexpected error occurred while fetching favorite listings."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
def to_homepage(request):
    # If the user is authenticated, redirect to another page or display a welcome message
    context = {
        "is_authenticated": request.user.is_authenticated,
        "user": request.user if request.user.is_authenticated else None,
    }
    return render(request, 'api/homepage.html', context)