CREATE TABLE IF NOT EXISTS users(
    UID INTEGER PRIMARY KEY,
    user_state TEXT,
    latitude REAL,
    longitude REAL,
    distance INTEGER,
    notified TEXT
)