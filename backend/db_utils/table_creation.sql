-- Make User table
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    location TEXT,
    image TEXT
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

-- UserFavoriteListing 
CREATE TABLE IF NOT EXISTS UserFavoriteListing (
    listing_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES Listing(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    PRIMARY KEY (listing_id, user_id)
    )

-- UserBlock
CREATE TABLE IF NOT EXISTS UserBlock (
    blocker_id INTEGER NOT NULL,
    blocked_id INTEGER NOT NULL,
    FOREIGN KEY (blocker_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (blocked_id) REFERENCES User(id) ON DELETE CASCADE,
    PRIMARY KEY (blocker_id, blocked_id)
);

-- TODO: Make tables for messages


DROP TABLE Listing
DROP TABLE Tag
DROP TABLE ListingTag
