#api/authentication.py
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from django.contrib.auth.hashers import check_password
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from jwt import InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import User

'''
CLASSES: 
CustomJWTAuthentication, 
'''

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, user_token):
        """ Override get_user to retrieve user from custom database instead of Django's ORM.

        Args:
            user_token (JWTToken): A JWT token with data about the associated user.

        Raises:
            InvalidTokenError: Occurs when the token doesn't contain the identifying info.
            AuthenticationFailed: The token is invalid in some way.

        Returns:
            User: The authenticated user.
        """

        try:
            user_id = user_token["user_id"]
        except KeyError:
            raise InvalidTokenError(_("Token contained no recognizable user identification"))
        
        user_data = db_query.get_user_by_id(user_id)

        if user_data is None:
            raise AuthenticationFailed("User not found.")
        return User(**user_data)

    @staticmethod
    def validate_user_credentials(username, password):
        """ Validate username and password.
        """

        # get user from db
        try:
            user_data = db_query.get_user_by_username(username)
        except IndexError:
            # User doesn't exist
            return None

        # Check password
        if user_data and check_password(password, user_data["password"]):
            return User(**user_data)


class CustomJWTAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "api.authentication.CustomJWTAuthentication"
    name = "CustomJWTAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT-based authentication using a Bearer token.",
        }