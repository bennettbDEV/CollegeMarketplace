from abc import ABC, abstractmethod
from db_utils.connections import SQLiteConnection


class DBQuery(ABC):
    def __init__(self, db_connection):
        self.db_connection = db_connection

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


class SQLiteDBQuery(DBQuery):
    # Listings functions
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
        query = "SELECT * FROM User WHERE id = ?"
        params = (user_id,)
        self.db_connection.connect()
        user = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        return user
    
    def get_user_by_username(self, username):
        query = "SELECT * FROM User WHERE username = ?"
        params = (username,)
        self.db_connection.connect()
        user = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
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