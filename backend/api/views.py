from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from .serializers import UserSerializer, ListingSerializer
from .models import Listing, User
from .serializers import CustomTokenObtainPairSerializer

# added by Chase (will need to edit)
from .user_handler import UserHandler

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    # Login request
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # If valid credentials
        if serializer.is_valid():
            user_data = serializer.validated_data

            if user_data:
                # Get users id
                user = db_query.get_user_by_username(user_data["username"])[0]
                user_data["id"] = user["id"]

                # Create tokens for the authenticated user
                refresh = RefreshToken.for_user(User(**user_data))
                access_token = str(refresh.access_token)

                # Return tokens in the response
                return Response(
                    {
                        "access": access_token,
                        "refresh": str(refresh),
                    }
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        # If the serializer is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        # User must be authenticated if performing any action other than create/retrieve/list
        self.permission_classes = (
            [AllowAny]
            if (self.action in ["create", "list", "retrieve"])
            else [IsAuthenticated]
        )
        return super().get_permissions()

    def get_queryset(self):
        # Gets all users
        users = db_query.get_all_users()
        # ** operator is used to pass all key value pairs to the calling function
        return [User(**user) for user in users]

    # Crud actions
    def list(self, request):
        users = db_query.get_all_users()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    # User registration
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Check if user already exists
            username = validated_data["username"]
            if db_query.get_user_by_username(username):
                return Response(
                    {"detail": "Username already exists."},
                    status=status.HTTP_409_CONFLICT,
                )
            # Generate password
            validated_data["password"] = make_password(validated_data["password"])

            # Create user
            db_query.create_user(serializer.validated_data)

            # Get users id
            user = db_query.get_user_by_username(username)[0]
            validated_data["id"] = user["id"]

            # Generate JWT token for the new user
            refresh = RefreshToken.for_user(User(**validated_data))
            access = str(refresh.access_token)

            # Form response
            return Response(
                {
                    "access": access,
                    "refresh": str(refresh),
                },
                status=201,
            )

        else:
            return Response(serializer.errors, status=400)


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
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            db_query.create_listing(serializer.validated_data, user_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        listing = db_query.get_listing_by_id(pk)
        if listing:
            serializer = self.get_serializer(listing)
            return Response(serializer.data)
        return Response(status=404)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        db_query.delete_listing(pk)
        return Response(status=204)
