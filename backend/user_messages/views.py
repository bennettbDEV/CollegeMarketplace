# api/views.py
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

from .message_mediators import MessageMediator
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.GenericViewSet):
    serializer_class = MessageSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_mediator = MessageMediator()

    # retrieve message for one user
    def retrieve(self, request, pk=None):
        """Retrieves the specified Message.
        Args:
            request (request): DRF request object, must have message id
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """

        message = self.message_mediator.retrieve_message(MessageMediator, request)
        if message:
            serializer = Message(
                message.id, message.sender, message.receiver, message.content
            )
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Message with that id from that User is not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # retrieve all message for one user
    def list(self, request):
        """Retrieves all messages received by the calling user.
        Args:
            request (Request): DRF request object
        Returns:
            Response: A DRF Response object with an HTTP status.
        """

        # Gets all messages and return it -> could be modified later to be filtered
        messages = self.message_mediator.retrieve_all_messages(request)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete a message from a user(who retrieved it) given message id and user
    def destroy(self, request, pk=None):
        """Deletes the specified Message.

        Args:
            request (Request): DRF request object, must have message id.
            pk (int, optional): The id of the User.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """

        try:
            response = self.message_mediator.delete_message(
                MessageMediator, request.id, request.user.id
            )
            return response
        except Exception as e:
            print(str(e))
            return Response(
                {"error": "Server error occured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # create and send message from one user to another
    def create(self, request):
        """Creates and sends a message from a sender to a receiver User.
        Args:
            request (Request): DRF request object, must have receiver(User Object) and content for message
            pk (int, optional): The id of the recieving User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """

        serializer = self.get_serializer(data=request.data)
        # check if data is valid
        if serializer.is_valid():
            user_id = request.user.id
            response = self.message_mediator.send_message(serializer.validated_data, user_id)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
