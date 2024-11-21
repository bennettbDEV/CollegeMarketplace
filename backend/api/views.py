# api/views.py
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .handlers import ListingHandler, UserHandler
from .models import Listing, User
from .serializers import ListingSerializer, LoginSerializer, UserSerializer


# CustomTokenObtainPairView
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # Login request
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # If valid credentials
        if serializer.is_valid():
            user_data = serializer.validated_data
            response = UserHandler.login(UserHandler,user_data)
            return response
        
        # If the serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        # User must be authenticated if performing any action other than create/list/retrieve
        self.permission_classes = ([AllowAny] if (self.action in ["create", "list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        # Gets all users
        users = UserHandler.list_users(UserHandler)
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

        users = UserHandler.list_users(UserHandler)
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

            response = UserHandler.register_user(UserHandler, validated_data)
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

        user = UserHandler.get_user(UserHandler, pk)
        if user:
            serializer = self.get_serializer(User(**user))
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
            response = UserHandler.partial_update_user(UserHandler, request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        """Deletes the specified User.

        Args:
            request (Request): DRF request object.
            pk (int, optional): The id of the User. Defaults to None.

        Returns:
            Resposne: A DRF Response object with an HTTP status.
        """
        try:
            response = UserHandler.delete_user(UserHandler, request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Listing controller/handler
class ListingViewSet(viewsets.GenericViewSet):
    serializer_class = ListingSerializer
    
    def get_permissions(self):
        # User must be authenticated if performing any action other than retrieve/list
        self.permission_classes = ([AllowAny] if (self.action in ["list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def get_queryset(self):
        # Gets all listings -> could be modified later to be filtered
        listings = ListingHandler.list_listings(ListingHandler)
        return [Listing(**listing) for listing in listings]


    # Crud actions
    def list(self, request):
        listings = ListingHandler.list_listings(ListingHandler)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            response = ListingHandler.create_listing(ListingHandler, serializer.validated_data, user_id)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        listing = ListingHandler.get_listing(ListingHandler, pk)
        if listing:
            serializer = self.get_serializer(Listing(**listing))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Listing with that id not found."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            response = ListingHandler.partial_update_listing(ListingHandler, request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            response = ListingHandler.delete_listing(ListingHandler, request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
Non-class Related Functions 
'''

# Function to return to the generate the homepage
def to_homepage(request):
    return render(request, 'api/homepage.html',{}) #this naming convention is so stupid imo
