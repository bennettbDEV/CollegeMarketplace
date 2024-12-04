import sqlite3
from abc import ABC, abstractmethod
'''
CLASSES: 
DBConnection, SQLiteConnection
'''

class DBConnection(ABC):
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def execute_query(self, query, params=None):
        pass

    @abstractmethod
    def __enter__(self):
        pass
    
    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class SQLiteConnection(DBConnection):
    def connect(self):
        try:
            if not self.connection:
                self.connection = sqlite3.connect(self.db_config["NAME"])
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        try:
            self.connect()
            self.connection.row_factory = sqlite3.Row  # Enables accessing columns by name
            
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                # For INSERT, UPDATE, DELETE queries
                self.connection.commit()
                return cursor.rowcount  # Return number of rows affected
        except sqlite3.Error as e:
            print(f"An error occurred during query execution: {e}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
