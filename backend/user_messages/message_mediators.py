# message_mediator.py (created by trevin :3)
from abc import ABC, abstractmethod

from api.models import User
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from rest_framework import status
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


# Mediator Abstract Class
class Mediator(ABC):
    @abstractmethod
    def retrieve_messages(self, request):
        pass

    @abstractmethod
    def create_message(self, sender, receiver, content):
        pass

    @abstractmethod
    def delete_message(self, request, message_id):
        pass

    @abstractmethod
    def send_message(self, sender, receiver, content):
        pass

    @abstractmethod
    def query_user(self, user_id):
        pass


# message mediator class
class MessageMediator(Mediator):
    # retrieve all messages from a given user(request given, get user from that)
    def retrieve_all_messages(self, request):
        # no reason to check user, will use the requesting users id anyways
        messages = db_query.retrieve_all_messages(int(request.user.id))
        return [Message(**message) for message in messages]

    # retrieve a message from a given user(request given, get user from that)
    def retrieve_message(self, request, pk):
        # no reason to check user, will use the requesting users id anyways
        return db_query.get_message(int(request.message.id), pk)

    # creates message given sender(user), receiver(user), and content, and returns message id
    def create_message(self, sender, receiver, content):
        try:
            message = db_query.create_message(sender.id, receiver.id, content)
            return Response(message, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return Response(
                {"error": "Server error occured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # delete message given user id and message id
    def delete_message(self, request, message_id):
        # get users id from request
        user_id = request.user.id
        # query message
        message = db_query.get_message(message_id, user_id)
        # sanity check for message
        if not message:
            return Response(
                {"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND
            )
        # making sure person trying to delete the message is the receiver of the message
        if user_id == int(message.receiver_id):
            db_query.delete_message(message_id, user_id)
            return Response(
                {"detail": "Message deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN
            )

    # send message with sender(user), receiver(user), and content of the message
    def send_message(self, request, pk):
        receiver_id = request.receiver.id
        content = request.content
        if receiver_id == pk:
            # 0 is a placeholder, id will be generated on message creation
            serializer = MessageSerializer(0, pk, receiver_id, content)
            if serializer.is_valid():
                message = db_query.create_message(pk, receiver_id, content)
                return Response(
                    {"detail": "Message sent successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN
            )

    # query user given user id from the database
    def query_user(self, user_id):
        # query user via ID
        user = db_query.get_user_by_id(user_id)
        if not user:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return user
