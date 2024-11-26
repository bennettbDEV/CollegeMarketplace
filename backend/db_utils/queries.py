from abc import ABC, abstractmethod


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
            listing_dict = {column: row[column] for column in row.keys() if column != "tags"}
            listing_dict["tags"] = row["tags"].split(",") if row["tags"] else []
            listings.append(listing_dict)

        return listings

    def create_listing(self, data, user_id):
        listing_data = {key:value for key,value in data.items() if key != "tags"}
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
                tag_id = cursor.execute("SELECT id FROM Tag WHERE name = ?", (tag,)).fetchone()[0]

                # Add tag to listing
                listing_tag_query = "INSERT INTO ListingTag (listing_id, tag_id) VALUES (?, ?);"
                cursor.execute(listing_tag_query, (listing_id, tag_id))
            
            # Save change
            db.connection.commit()

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
        listing_dict = {column: row[column] for column in row.keys() if column != "tags"}
        listing_dict["tags"] = row["tags"].split(",") if row["tags"] else []

        return listing_dict
    
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
            listing_dict = {column: row[column] for column in row.keys() if column != "tags"}
            listing_dict["tags"] = row["tags"].split(",") if row["tags"] else []
            listings.append(listing_dict)

        return listings

    def partial_update_listing(self, listing_id, new_data):
        # Get tag(s) data if it exists
        tags = new_data.pop("tags", None)

        # Exclude id, likes, and dislikes:
        exclude = ["id","likes","dislikes"]
        new_data = {key: value for key, value in new_data.items() if key not in exclude}

        # Dynamically generate a string for each column
        columns = ", ".join(f"{key} = ?" for key in new_data.keys())
        # Use the generated string to update all specified columns
        query = f"UPDATE Listing SET {columns} WHERE id = ?"
        params = tuple(new_data.values()) + (listing_id,)

        
        with self.db_connection as db:
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

                    listing_tag_query = "INSERT INTO ListingTag (listing_id, tag_id) VALUES (?, ?);"
                    db.execute_query(listing_tag_query, (listing_id, tag_id))

    def delete_listing(self, listing_id):
        query = "DELETE FROM listing WHERE id = ?"
        params = (listing_id,)
        with self.db_connection as db:
            db.execute_query(query, params)

    # TODO: Write queries for adding, deleting, and retrieving listings to/from UserFavoriteListing
    def add_favorite_listing(self, user_id, listing_id):
        query = """
            INSERT INTO UserFavoriteListing (user_id, listing_id) 
            VALUES (?, ?)
            """
        params = (user_id, listing_id)
        with self.db_connection as db:
            db.execute_query(query, params)

    def remove_favorite_listing(self, user_id, listing_id):
        pass

    def retrieve_favorite_listings(self, user_id):
        pass

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
            INSERT INTO User (username, password, location) 
            VALUES (?, ?, ?)
            """
            params = (data["username"], data["password"], data["location"])
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
        return user

    def get_user_by_username(self, username):
        query = "SELECT * FROM User WHERE username = ? LIMIT 1"
        params = (username,)

        with self.db_connection as db:
            user = db.execute_query(query, params)

        # The query returns a list of user rows, so return actual user instance
        if user:
            user = user[0]
        return user

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

