-- Make User table
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    location TEXT
);

-- Make Listing table
CREATE TABLE IF NOT EXISTS Listing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    condition TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL,
    likes INTEGER DEFAULT 0 NOT NULL,
    dislikes INTEGER DEFAULT 0 NOT NULL,
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (author_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ListingTag (
    listing_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES Listing(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tag(id) ON DELETE CASCADE,
    PRIMARY KEY (listing_id, tag_id)
);

-- TODO: MAKE UserFavoriteListing table



DROP TABLE Listing
DROP TABLE Tag
DROP TABLE ListingTag