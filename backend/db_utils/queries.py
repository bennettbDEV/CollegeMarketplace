from abc import ABC, abstractmethod
from db_utils.connections import SQLiteConnection


class DBQuery(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DBQuery, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_connection):
        # Avoid reinitializing
        if not hasattr(self, "_initialized"):
            self.db_connection = db_connection
            self._initialized = True

    @abstractmethod
    def get_all_listings(self):
        pass

    @abstractmethod
    def create_listing(self, data, user_id):
        pass

    @abstractmethod
    def get_user_listings(self, user_id):
        pass

    @abstractmethod
    def delete_listing(self, listing_id):
        pass

    @abstractmethod
    def get_user_by_id(self, listing_id):
        pass


# We need to refactor our queries to avoid connecting and disconnecting to the db every time
class SQLiteDBQuery(DBQuery):
    # Listing functions
    def get_all_listings(self):
        query = "SELECT * FROM listing"
        self.db_connection.connect()
        listings = self.db_connection.execute_query(query)
        self.db_connection.disconnect()
        return listings

    def create_listing(self, data, user_id):
        query = """
        INSERT INTO listing (title, description, created_at, author_id) 
        VALUES (?, ?, CURRENT_TIMESTAMP, ?)
        """
        params = (data["title"], data["description"], user_id)
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()

    def get_user_listings(self, user_id):
        query = "SELECT * FROM listing WHERE author_id = ?"
        params = (user_id,)
        self.db_connection.connect()
        listings = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        return listings

    def delete_listing(self, listing_id):
        query = "DELETE FROM listing WHERE id = ?"
        params = (listing_id,)
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()


    # User functions
    def get_all_users(self):
        query = "SELECT * FROM user"
        self.db_connection.connect()

        rows = self.db_connection.execute_query(query)
        self.db_connection.disconnect()

        # Turn data from rows into a list of dicts
        users = [{column: row[column] for column in row.keys()} for row in rows]

        return users

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM User WHERE id = ? LIMIT 1"
        params = (user_id,)
        self.db_connection.connect()
        user = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        
        # The query returns a list of user rows, so return actual user instance
        if user:
            user = user[0]
        return user

    def get_user_by_username(self, username):
        query = "SELECT * FROM User WHERE username = ? LIMIT 1"
        params = (username,)
        self.db_connection.connect()
        user = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()

        # The query returns a list of user rows, so return actual user instance
        if user:
            user = user[0]
        return user

    def create_user(self, data):
        query = """
        INSERT INTO User (username, password, location) 
        VALUES (?, ?, ?)
        """
        params = (data["username"], data["password"], data["location"])
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()

    def delete_user(self, user_id):
        query = "DELETE FROM user WHERE id = ?"
        params = (user_id,)
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()

    def partial_update_user(self, user_id, new_data):
        # Exclude "id" key:value pair. We should not modify user's id
        new_data = {key: value for key, value in new_data.items() if key != "id"}
        # Dynamically generate a string for each column
        columns = ", ".join(f"{key} = ?" for key in new_data.keys())
        # Use the generated string to update all specified columns
        query = f"UPDATE user SET {columns} WHERE id = ?"
        params = tuple(new_data.values()) + (user_id,)

        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()