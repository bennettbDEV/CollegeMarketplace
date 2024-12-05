# user_messages/views.py
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .message_mediators import MessageMediator
from .models import Message
from .serializers import MessageSerializer

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


class MessageViewSet(viewsets.GenericViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_mediator = MessageMediator()

    # check if person is the sender or retriever
    def check_permissions(self):
        pass

    # send message from one user to another
    def send_message(self, request, pk):
        """Creates and sends a message from a sender to a receiver User.
        Args:
            request (Request): DRF request object, must have receiver(User Object) and content for message
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        # is a placeholder rn, might change serializer
        serializer = Message(0, pk, request.receiver.id, request.content)
        # check if data is valid
        if serializer.is_valid():
            response = self.message_mediator.send_message(MessageMediator, request, pk)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # retrieve message for one user
    def retrieve(self, request, pk=None):
        """Retrieves the specified Message.
        Args:
            request (Request): DRF request object, must have message id
            pk (int, optional): The id of the User.
        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        message = self.message_mediator.retrieve_message(MessageMediator, request, pk)
        if message:
            serializer = Message(
                message.id, message.sender, message.receiver, message.content
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Message with that id from that User is not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # retrieve all message for one user
    def list(self, request, pk=None):
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

    # delete a message from a user(who retrieved it) given message id and user
    def destroy(self, request, pk):
        """Deletes the specified Message.

        Args:
            request (Request): DRF request object, must have message id.
            pk (int, optional): The id of the User.

        Returns:
            Response: A DRF Response object with an HTTP status.
        """
        try:
            response = self.message_mediator.delete_user(
                MessageMediator, request.id, pk
            )
            return response
        except Exception as e:
            print(str(e))
            return Response(
                {"error": "Server error occured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
