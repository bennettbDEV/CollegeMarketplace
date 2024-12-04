#api/views.py
# api/views.py
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

#imports
from .message_mediators import MessageMediator
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.GenericViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_mediator = MessageMediator()
    #retrieve message for one user
    def retrieve(self, request, pk):
        """Retrieves the specified Message.
        Args:
            request (Request): DRF request object, must have message id
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        message = self.message_mediator.retrieve_message(MessageMediator, request)
        if message:
            serializer = Message(message.id, message.sender, message.receiver, message.content)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Message with that id from that User is not found."}, status=status.HTTP_404_NOT_FOUND)
    #retrieve all message for one user
    def list(self, request, pk):
        """Retrieves all messages received by a User.
        Args:
            request (Request): DRF request object
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        # Gets all messages and return it -> could be modified later to be filtered
        messages = self.message_mediator.retrieve_all_messages(MessageMediator, request)
        return messages
    #delete a message from a user(who retrieved it) given message id and user
    def delete(self, request, pk):
        """Deletes the specified Message.

        Args:
            request (Request): DRF request object, must have message id.
            pk (int, optional): The id of the User.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            response = self.message_mediator.delete_user(MessageMediator, request.id, pk)
            return response
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #send message from one user to another
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_message(self, request, pk):
        """Creates and sends a message from a sender to a receiver User.
        Args:
            request (Request): DRF request object, must have receiver(User Object) and content for message
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        #is a placeholder rn, might change serializer
        serializer = Message(0, request.user.id, request.receiver.id, request.content)
        #check if data is valid
        if serializer.is_valid():
            response = self.message_mediator.send_message(MessageMediator, request.user.id, request.receiver.id, request.content)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

