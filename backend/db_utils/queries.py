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
        query = """
        SELECT l.id, l.title, l.description, l.price, l.image, l.author_id, l.created_at,
        GROUP_CONCAT(t.name) AS tags
        FROM Listing l
        LEFT JOIN ListingTag lt ON l.id = lt.listing_id
        LEFT JOIN Tag t ON lt.tag_id = t.id
        GROUP BY l.id, l.title, l.description, l.price, l.image, l.author_id, l.created_at;
        """
        self.db_connection.connect()
        rows = self.db_connection.execute_query(query)
        self.db_connection.disconnect()

        listings = []
        for row in rows:
            listing_dict = {column: row[column] for column in row.keys() if column != "tags"}
            listing_dict["tags"] = row["tags"].split(",") if row["tags"] else []
            listings.append(listing_dict)

        return listings


    def create_listing(self, data, user_id):
        listing_data = {key:value for key,value in data.items() if key != "tags"}
        query = """
        INSERT INTO Listing (title, description, price, image, author_id)
        VALUES (?, ?, ?, ?, ?);
        """
        params = (listing_data["title"],listing_data["description"],
                listing_data["price"], listing_data["image"], user_id)
        
        self.db_connection.connect()
        cursor = self.db_connection.connection.cursor()
        # Add listing
        cursor.execute(query, params)

        # Get id of inserted listing
        listing_id = cursor.lastrowid

        # Add tags
        # If tag doesn't exit, add it to the Tag table
        tag_query = "INSERT OR IGNORE INTO Tag (name) VALUES (?);"
        for tag in data["tags"]:
            cursor.execute(tag_query, (tag,))
            # Get relevent tag id
            tag_id = cursor.lastrowid or cursor.execute("SELECT id FROM Tag WHERE name = ?", (tag,)).fetchone()[0]

            # Add tag to listing
            listing_tag_query = "INSERT INTO ListingTag (listing_id, tag_id) VALUES (?, ?);"
            cursor.execute(listing_tag_query, (listing_id, tag_id))

            self.db_connection.connection.commit()
        
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



    # --------------------------------------------------------------------------------

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