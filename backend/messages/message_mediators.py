#message_mediator.py (created by trevin :3)
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MessageSerializer
from .models import Message
from ..api.models import User

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))

#mediator class
class MessageMediator:

    #send message with sender_id, receiver_id, and content of the message
    def send_message(sender_id, receiver_id, content):
        pass

    #retrieve all messages from a given user
    def retrieve_messages(user):
        pass

    #creates message given sender, receiver, and content, and returns message id
    def create_message(self, sender_id, receiver_id, content):
       try:
            message = db_query.create_message()
            return Response(message, status=status.HTTP_201_CREATED)
       except Exception as e:
            print(str(e))
            return Response({"error": "Server error occured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #delete message given user id and message id
    def delete_message(user_id, message_id):
        pass

    #query user given user id from the database
    def query_user(user_id):
        #query user via ID
        user = db_query.get_user_by_id(user_id)
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return user
