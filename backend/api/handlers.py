# user_handler.py (created by CHASE)
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from .models import User 
# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))

class UserHandler:
    def __init__(self, user):
        self.user = user

    # login function
    def login(self, username, password):
        # Implement login logic here. EDIT as this is basic
        if self.user.username == username and check_password(password, self.user.password):
            return True
        else:
            return False

    # logout function
    def logout(self):
        # Implement logout logic here (e.g., clear session or tokens) EDIT LATER
        pass



    def register_user(validated_data):
        # Check if user already exists
        new_username = validated_data["username"]
        if db_query.get_user_by_username(new_username):
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        # Generate password
        validated_data["password"] = make_password(validated_data["password"])

        # Create user
        db_query.create_user(validated_data)

        # Get users id
        user = db_query.get_user_by_username(new_username)
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
            status=status.HTTP_201_CREATED,
        )

    # update_account function
    def update_account(self, username, password):
        # Add logic later
        pass

    # update_account function
    def do_stuff(self):
        # Add logic later
        pass


class LoginHandler:
    pass
