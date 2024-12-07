#db_utils/queries.py
'''
CLASSES: 
DBQuery, SQLiteDBQuery
'''
from abc import ABC, abstractmethod
from django.conf import settings

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

    # Listing methods
    @abstractmethod
    def get_all_listings(self):
        pass

    @abstractmethod
    def create_listing(self, data, user_id):
        pass

    @abstractmethod
    def get_listing_by_id(self, listing_id):
        pass

    @abstractmethod
    def partial_update_listing(self, listing_id, new_data):
        pass

    @abstractmethod
    def delete_listing(self, listing_id):
        pass

    # User methods
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def create_user(self, data):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def partial_update_user(self, user_id, new_data):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass


# We need to refactor our queries to avoid connecting and disconnecting to the db every time
class SQLiteDBQuery(DBQuery):
    # Listing methods
    def get_all_listings(self):
        query = """
        SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
        GROUP_CONCAT(t.name) AS tags
        FROM Listing l
        LEFT JOIN ListingTag lt ON l.id = lt.listing_id
        LEFT JOIN Tag t ON lt.tag_id = t.id
        GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at;
        """

        with self.db_connection as db:
            rows = db.execute_query(query)

        listings = []
        for row in rows:
            listing = {column: row[column] for column in row.keys() if column != "tags"}
            listing["tags"] = row["tags"].split(",") if row["tags"] else []
            listing["image"] = f"{settings.MEDIA_URL}{listing['image']}"

            listings.append(listing)
        return listings

    def get_filtered_listings(self, filters=None, search_term=None, ordering=None):
        query = """
        SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
        GROUP_CONCAT(t.name) AS tags
        FROM Listing l
        LEFT JOIN ListingTag lt ON l.id = lt.listing_id
        LEFT JOIN Tag t ON lt.tag_id = t.id
        WHERE 1=1 --<filters>
        GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at
        """

        params = []

        filter_clauses = ""
        # Apply filters to the query
        if filters:
            for field, value in filters.items():
                operator = "="
                if field.startswith("min"):
                    operator = ">="
                    field = field[(field.find("_")+1):]
                    value = int(value)
                elif field.startswith("max"):
                    operator = "<="
                    field = field[(field.find("_")+1):]
                    value = int(value)

                filter_clauses += f" AND {field} {operator} ?"
                params.append(value)

        # Apply search term if provided (e.g., filter by title or description)
        if search_term:
            filter_clauses += (
                " AND (title LIKE ? OR description LIKE ? OR t.name LIKE ?)"
            )
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])

        query = query.replace("--<filters>", filter_clauses)

        # Apply ordering if provided
        if ordering:
            # Prefix with '-' for descending order
            descending = ordering.startswith("-")
            field_name = ordering.lstrip("-")  # Remove '-' if exists

            # Ensure the field name is valid
            valid_fields = [
                "title",
                "condition",
                "description",
                "price",
                "likes",
                "dislikes",
                "created_at",
            ]
            if field_name.lower() in valid_fields:
                query += f" ORDER BY {field_name}"
                if descending:
                    query += " DESC"
                else:
                    query += " ASC"

        with self.db_connection as db:
            rows = db.execute_query(query, params)

        listings = []
        for row in rows:
            listing = {column: row[column] for column in row.keys() if column != "tags"}
            listing["tags"] = row["tags"].split(",") if row["tags"] else []
            listing["image"] = f"{settings.MEDIA_URL}{listing['image']}"

            listings.append(listing)
        return listings

    def create_listing(self, data, user_id):
        listing_data = {key: value for key, value in data.items() if key != "tags"}
        query = """
        INSERT INTO Listing (title, condition, description, price, image, author_id)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        # Likes and dislikes are set to 0 when created in db
        params = (
            listing_data["title"],
            listing_data["condition"],
            listing_data["description"],
            listing_data["price"],
            listing_data["image"],
            user_id,
        )

        with self.db_connection as db:
            cursor = db.connection.cursor()
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
                tag_id = cursor.execute(
                    "SELECT id FROM Tag WHERE name = ?", (tag,)
                ).fetchone()[0]

                # Add tag to listing
                listing_tag_query = (
                    "INSERT INTO ListingTag (listing_id, tag_id) VALUES (?, ?);"
                )
                cursor.execute(listing_tag_query, (listing_id, tag_id))

            # Save change
            db.connection.commit()
            return listing_id

    def get_listing_by_id(self, listing_id):
        query = """
        SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
        GROUP_CONCAT(t.name) AS tags
        FROM Listing l
        LEFT JOIN ListingTag lt ON l.id = lt.listing_id
        LEFT JOIN Tag t ON lt.tag_id = t.id
        WHERE l.id = ?
        GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at;
        """

        with self.db_connection as db:
            rows = db.execute_query(query, (listing_id,))

        if not rows:
            return None

        row = rows[0]
        listing = {column: row[column] for column in row.keys() if column != "tags"}
        listing["tags"] = row["tags"].split(",") if row["tags"] else []
        listing["image"] = f"{settings.MEDIA_URL}{listing['image']}"

        return listing

    def get_listing_by_author_id(self, author_id):
        query = """
        SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
        GROUP_CONCAT(t.name) AS tags
        FROM Listing l
        LEFT JOIN ListingTag lt ON l.id = lt.listing_id
        LEFT JOIN Tag t ON lt.tag_id = t.id
        WHERE l.author_id = ?
        GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at;
        """

        with self.db_connection as db:
            rows = db.execute_query(query, (author_id,))

        listings = []
        for row in rows:
            listing_dict = {
                column: row[column] for column in row.keys() if column != "tags"
            }
            listing_dict["tags"] = row["tags"].split(",") if row["tags"] else []
            listings.append(listing_dict)

        return listings

    def partial_update_listing(self, listing_id, new_data):
        # Get tag(s) data if it exists
        tags = new_data.pop("tags", None)

        # Exclude id, likes, and dislikes:
        exclude = ["id", "likes", "dislikes"]
        new_data = {key: value for key, value in new_data.items() if key not in exclude}

        # Dynamically generate a string for each column
        columns = ", ".join(f"{key} = ?" for key in new_data.keys())
        
        # Use the generated string to update all specified columns
        query = f"UPDATE Listing SET {columns} WHERE id = ?"
        params = tuple(new_data.values()) + (listing_id,)

        with self.db_connection as db:
            if new_data:
                db.execute_query(query, params)

            # Update tags
            if tags:
                # Remove existing tags for the listing
                delete_query = "DELETE FROM ListingTag WHERE listing_id = ?"
                db.execute_query(delete_query, (listing_id,))

                # Add new tags
                for tag in tags:
                    # If tag doesn't exit, add it to the Tag table
                    tag_query = "INSERT OR IGNORE INTO Tag (name) VALUES (?);"
                    db.execute_query(tag_query, (tag,))

                    tag_id_query = "SELECT id FROM Tag WHERE name = ?;"
                    tag_id = db.execute_query(tag_id_query, (tag,))[0]["id"]

                    listing_tag_query = (
                        "INSERT INTO ListingTag (listing_id, tag_id) VALUES (?, ?);"
                    )
                    db.execute_query(listing_tag_query, (listing_id, tag_id))

    def delete_listing(self, listing_id):
        query = "DELETE FROM listing WHERE id = ?"
        params = (listing_id,)
        with self.db_connection as db:
            db.execute_query(query, params)


    '''
    Favorite Listing Content
    '''
    def add_favorite_listing(self, user_id, listing_id):
        query = """
            INSERT INTO UserFavoriteListing (user_id, listing_id) 
            VALUES (?, ?)
            """
        params = (user_id, listing_id)
        with self.db_connection as db:
            db.execute_query(query, params)
            
    #Function: query to remove a favorite listing 
    def remove_favorite_listing(self, user_id, listing_id):
        """
        Removes a favorite listing for the given user.

        Args:
            user_id (int): The ID of the user.
            listing_id (int): The ID of the listing to be removed.

        Returns:
            None: The function executes the SQL query and commits changes.
        """
        query = """
            DELETE FROM UserFavoriteListing 
            WHERE user_id = ? AND listing_id = ?
        """
        params = (user_id, listing_id)
        
        with self.db_connection as db:
            db.execute_query(query, params)

    #Function: query to retrieve a list of the user's favorite listings 
    def retrieve_favorite_listings(self, user_id):
        """
        Retrieves all favorite listings for a given user.

        Args:
            user_id (int): The ID of the user whose favorites are being fetched.

        Returns:
            list: A list of dictionaries containing details of the user's favorite listings.
        """
        query = """
            SELECT l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at,
            GROUP_CONCAT(t.name) AS tags
            FROM UserFavoriteListing ufl
            INNER JOIN Listing l ON ufl.listing_id = l.id
            LEFT JOIN ListingTag lt ON l.id = lt.listing_id
            LEFT JOIN Tag t ON lt.tag_id = t.id
            WHERE ufl.user_id = ?
            GROUP BY l.id, l.title, l.condition, l.description, l.price, l.image, l.likes, l.dislikes, l.author_id, l.created_at;
        """
        params = (user_id,)
        
        with self.db_connection as db:
            rows = db.execute_query(query, params)

        # Process rows into a list of favorite listings
        favorite_listings = []
        for row in rows:
            listing = {column: row[column] for column in row.keys() if column != "tags"}
            listing["tags"] = row["tags"].split(",") if row["tags"] else []
            favorite_listings.append(listing)

        return favorite_listings


    '''
    Block / Unblock Content
    '''
    # TODO - ensure this is checked within message 
    #Function: block a user 
    def block_user(self, blocker_id, blocked_id):
        """
        Adds a user to the blocker's block list.

        Args:
            blocker_id (int): The ID of the user blocking another user.
            blocked_id (int): The ID of the user to be blocked.

        Returns:
            dict: A dictionary with the result message and HTTP status.
        """
        query = """
            INSERT INTO UserBlock (blocker_id, blocked_id) 
            VALUES (?, ?) ON CONFLICT DO NOTHING
        """
        params = (blocker_id, blocked_id)

        with self.db_connection as db:
            num_affected_rows = db.execute_query(query, params)
            return num_affected_rows

    #Function: unblock a user  
    def unblock_user(self, blocker_id, blocked_id):
        """
        Removes a user from the blocker's block list.

        Args:
            blocker_id (int): The ID of the user removing the block.
            blocked_id (int): The ID of the user being unblocked.

        Returns:
            dict: A dictionary with the result message and HTTP status.
        """
        query = """
            DELETE FROM UserBlock 
            WHERE blocker_id = ? AND blocked_id = ?
            ON CONFLICT DO NOTHING
        """
        params = (blocker_id, blocked_id)

        with self.db_connection as db:
            num_affected_rows = db.execute_query(query, params)
            return num_affected_rows

    #Function: check if user is blocked
    def is_user_blocked(self, sender_id, receiver_id):
        """
        Checks if the sender is blocked by the receiver.

        Args:
            sender_id (int): The ID of the user sending the message.
            receiver_id (int): The ID of the user receiving the message.

        Returns:
            bool: True if the sender is blocked, False otherwise.
        """
        query = """
            SELECT 1 
            FROM UserBlock 
            WHERE blocker_id = ? AND blocked_id = ?
        """
        params = (sender_id, receiver_id)

        with self.db_connection as db:
            result = db.execute_query(query, params)
            return bool(result)


    '''
    Like / Dislike Listing Content
    '''

    #Like and dislike queries:
    def like_listing(self, listing_id, current_likes):
        query = "UPDATE Listing SET likes = ? WHERE id = ?"
        params = (current_likes + 1, listing_id)

        with self.db_connection as db:
            db.execute_query(query, params)

    def dislike_listing(self, listing_id, current_dislikes):
        query = "UPDATE Listing SET dislikes = ? WHERE id = ?"
        params = (current_dislikes + 1, listing_id)

        with self.db_connection as db:
            db.execute_query(query, params)
            
    # --------------------------------------------------------------------------------

    # User methods
    def get_all_users(self):
        query = "SELECT * FROM user"

        with self.db_connection as db:
            rows = db.execute_query(query)

        # Turn data from rows into a list of dicts
        users = [{column: row[column] for column in row.keys()} for row in rows]
        return users

    def create_user(self, data):
        query = """
            INSERT INTO User (username, password, location, email, image) 
            VALUES (?, ?, ?, ?, ?)
            """
        params = (data["username"], data["password"], data["location"], data["email"], data["image"])
        with self.db_connection as db:
            db.execute_query(query, params)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM User WHERE id = ? LIMIT 1"
        params = (user_id,)
        with self.db_connection as db:
            user = db.execute_query(query, params)
        # The query returns a list of user rows, so return actual user instance
        if user:
            user = user[0]
            return dict(user)
        else:
            return None

    def get_user_by_username(self, username):
        query = "SELECT * FROM User WHERE username = ? LIMIT 1"
        params = (username,)

        with self.db_connection as db:
            user = db.execute_query(query, params)

        # The query returns a list of user rows, so return actual user instance
        if user:
            user = user[0]
        return dict(user)

    def partial_update_user(self, user_id, new_data):
        # Exclude "id" key:value pair. We should not modify user's id
        new_data = {key: value for key, value in new_data.items() if key != "id"}

        # Dynamically generate a string for each column
        columns = ", ".join(f"{key} = ?" for key in new_data.keys())

        # Use the generated string to update all specified columns
        query = f"UPDATE user SET {columns} WHERE id = ?"
        params = tuple(new_data.values()) + (user_id,)

        with self.db_connection as db:
            db.execute_query(query, params)

    def delete_user(self, user_id):
        query = "DELETE FROM user WHERE id = ?"
        params = (user_id,)
        with self.db_connection as db:
            db.execute_query(query, params)
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()

    # --------------------------------------------------------------------------------
    # Message functions

    #create message creates a message given sender, receiver, and content, then returns message id
    def create_message(self, sender_id, receiver_id, content):
        #create query and parameters
        query = """
        INSERT INTO message (sender, receiver, content) 
        VALUES (?, ?, ?)
        """
        params = (sender_id, receiver_id, content)
        #execute query
        self.db_connection.connect()
        self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        #attempt get new message ID without too much hassle and return it
    
    #delete message using message_id and receiver_id
    def delete_message(self, message_id, receiver_id):
        #query and param initialization
        query = "DELETE FROM message WHERE receiverID = ? AND messageID = ?"
        params = (receiver_id, message_id)
        #do query

    #get message from message_id and receiver_id
    def get_message(self, message_id, receiver_id):
        #make query and parameters
        query = "SELECT * FROM message WHERE receiverID = ? and messageID = ? LIMIT 1"
        params = (receiver_id, message_id)
        #execute query
        self.db_connection.connect()
        message = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        
        # The query returns a list of message rows, so return actual message instance
        if message:
            message = message[0]
        return message
    
    #gets all messages received by the user
    def get_all_messages(self, user_id):
        #make query and parameters
        query = "SELECT * FROM message WHERE receiverID = ?"
        params = (user_id)
        #do query
        self.db_connection.connect()
        messages = self.db_connection.execute_query(query, params)
        self.db_connection.disconnect()
        #return messages
        return messages
