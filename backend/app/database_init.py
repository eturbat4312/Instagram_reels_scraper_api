import sqlite3


def initialize_database():
    connection = sqlite3.connect("backend/app/database.db")
    cursor = connection.cursor()

    # Create the users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    # Create the reels table, linking to the users table
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS reels (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        reel_id TEXT,
        views INTEGER,
        likes INTEGER,
        comments INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
