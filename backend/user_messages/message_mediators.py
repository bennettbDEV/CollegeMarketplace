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
    def retrieve_all_messages(self, request, pk):
        pass

    @abstractmethod
    def retrieve_message(self, request):
        pass

    @abstractmethod
    def delete_message(self, user_id, message_id):
        pass

    @abstractmethod
    def send_message(self, sender, receiver, content):
        pass

    @abstractmethod
    def query_user(self, user_id):
        pass


# message mediator class
class MessageMediator(Mediator):
    #retrieve all messages from a given user(request given, get user from that)
    def retrieve_all_messages(self, request):
        #no reason to check user, will use the requesting users id anyways
        messages = db_query.get_all_messages(int(request.user.id))
        return [Message(**message) for message in messages]
    
    #retrieve a message from a given user(request given, get user from that)
    def retrieve_message(self, request):
        #no reason to check user, will use the requesting users id anyways
        return db_query.get_message(int(request.message.id), int(request.user.id))
    
    #delete message given user id and message id
    def delete_message(self, user_id, message_id):
        # query message
        message = db_query.get_message(message_id, user_id)
        # sanity check for message
        if not message:
            return Response(
                {"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND
            )
        # making sure person trying to delete the message is the receiver of the message
        if user_id == int(message['receiver_id']):
            db_query.delete_message(message_id, user_id)
            return Response(
                {"detail": "Message deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)
        
    #send message with sender(user), receiver(user), and content of the message
    def send_message(self, validated_data, sender_id):
        receiver_id = validated_data["receiver_id"]
        content = validated_data["content"]

        try:
            # Check if sender is sending a message to themself
            if sender_id == receiver_id:
                return Response({"error": "You cannot send a message to yourself."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if receiver exists
            if not db_query.get_user_by_id(receiver_id):
                return Response({"error": "Receiving user not found."}, status=status.HTTP_404_NOT_FOUND)

            # Receiver is valid so send message
            message_id = db_query.create_message(sender_id, receiver_id, content)
            validated_data["id"] = message_id
            return Response(validated_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #query user given user id from the database
    def query_user(self, user_id):
        # query user via ID
        user = db_query.get_user_by_id(user_id)
        if not user:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return user
