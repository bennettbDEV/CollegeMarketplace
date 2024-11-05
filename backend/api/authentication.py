from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from db_utils.db_factory import DBFactory, DBType
from db_utils.queries import SQLiteDBQuery
from api.models import User

# Initialize specific query object
db_query = SQLiteDBQuery(DBFactory.get_db_connection(DBType.SQLITE))

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, user_id):
        """
        Override get_user to retrieve user from custom database instead of Django's ORM.
        """
        user_data = db_query.get_user_by_id(user_id) 
        if user_data is None:
            raise AuthenticationFailed("User not found.")
        # Assuming user_data is a dictionary containing 'id' and 'username'
        return User(id=user_data['id'], username=user_data['username'])
    
def validate_user_credentials(username, password):
    # get user from db
    user_data = db_query.get_user_by_username(username)
    if user_data and check_password(password, user_data["password"]):
        return User(id=user_data['id'], username=user_data['username'])
    