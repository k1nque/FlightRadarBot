CREATE TABLE users(
    UID INTEGER PRIMARY KEY,
    user_state TEXT,
    latitude REAL,
    longitude REAL,
    distance INTEGER,
    notified BLOB
)