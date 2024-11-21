#api/views.py
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

#imports
from .message_mediators import MessageMediator
from .models import Message
from .serializers import MessageSerializer

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))

class MessageView:
    
    #check if person is the sender or retriever
    def check_permissions(self):
        pass
    #send message from one user to another
    def send_message(self, request):
        pass
    #retrieve message for one user
    def retrieve_message(self, request):
        pass
    #retrieve all message for one user
    def retrieve_all_messages(self, request):
        pass
