from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from .serializers import UserSerializer, ListingSerializer
from .models import Listing
from .serializers import CustomTokenObtainPairSerializer
#added by Chase (will need to edit)
from .user_handler import UserHandler

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        # User must be authenticated if performing any action other than create/retrieve/list
        self.permission_classes = ([AllowAny] if (self.action in ["create", "list", "retrieve"]) else [IsAuthenticated])
        return super().get_permissions()

    def list(self, request):
        users = db_query.get_all_users()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["password"] = make_password(validated_data["password"])
            db_query.create_user(serializer.validated_data)
            return Response(serializer.data, status=201)
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
