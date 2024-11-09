from jwt import InvalidTokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from api.models import User

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, user_token):
        """
        Override get_user to retrieve user from custom database instead of Django's ORM.
        """
        try:
            user_id = user_token["user_id"]
        except KeyError:
            raise InvalidTokenError(_("Token contained no recognizable user identification"))
        
        user_data = db_query.get_user_by_id(user_id)[0]

        if user_data is None:
            raise AuthenticationFailed("User not found.")
        return User(**user_data)


def validate_user_credentials(username, password):
    # get user from db
    user_data = db_query.get_user_by_username(username)[0]

    # Check password
    if user_data and check_password(password, user_data["password"]):
        return User(**user_data)
