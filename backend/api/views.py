#api/views.py
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from .serializers import UserSerializer, ListingSerializer
from .models import Listing, User
from .serializers import LoginSerializer

# added by Chase (will need to edit)
from .handlers import UserHandler

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))

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
        users = UserHandler.list_users(UserHandler)
        # Serialize data for all users -> format data as json
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    # User registration
    def create(self, request):
        # Serialize/Validate data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            response = UserHandler.register_user(UserHandler,validated_data)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = UserHandler.get_user(UserHandler, pk)
        if user:
            serializer = self.get_serializer(User(**user))
            return Response(serializer.data) # HTTP 200 OK
        return Response({"error": "User with that username not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # Needs some work still -> needs update_user() to be made in queries.py
    def update(self, request, pk=None):
        try:
            user = db_query.get_user_by_id(pk)
            if not user:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Ensure user is updating their own account
            if request.user.id == int(pk):
                serializer = self.get_serializer(User(**request.user))

                if serializer.is_valid():
                    # Ensure new username isnt taken
                    if db_query.get_user_by_username(request.user.username):
                        return Response({"error": "Username taken"}, status=status.HTTP_403_FORBIDDEN)

                db_query.update_user(pk, serializer.validated_data)
                return Response({"detail": "User edited successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        try:
            response = UserHandler.partial_update_user(UserHandler, request, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
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
        listings = db_query.get_all_listings()
        return [Listing(**listing) for listing in listings]


    # Crud actions
    def list(self, request):
        listings = db_query.get_all_listings()
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data) # HTTP 200 OK

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Create listing with reference to calling user's id
            user_id = request.user.id
            db_query.create_listing(serializer.validated_data, user_id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        listing = db_query.get_listing_by_id(pk)
        if listing:
            serializer = self.get_serializer(Listing(**listing))
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        try:
            listing = db_query.get_listing_by_id(pk)
            if not listing:
                return Response({"detail": "Listing not found."}, status=status.HTTP_404_NOT_FOUND) 
            
            # Ensure user is deleting their own listing
            if request.user.id == listing.author_id:
                db_query.delete_listing(pk)
                return Response({"detail": "Listing deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)
        
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
Non-class Related Functions 
'''

#Function to return to the generate the homepage 
def to_homepage(request):
    return render(request, 'api/homepage.html',{}) #this naming convention is so stupid imo