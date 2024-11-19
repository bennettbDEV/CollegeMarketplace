#api/views.py
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

#imports
from .models import Message
from .serializers import MessageSerializer

# Create your views here.
