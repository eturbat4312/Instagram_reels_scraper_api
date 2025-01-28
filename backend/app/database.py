import sqlite3


import logging

logging.basicConfig(level=logging.DEBUG)


def get_db_connection():
    db_path = "backend/app/database.db"
    logging.debug(f"Connecting to database at: {db_path}")  # Add this debug statement
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Optional for dict-like row access
    return conn


def get_reels(username):
    conn = get_db_connection()
    reels = conn.execute(
        "SELECT * FROM reels WHERE username = ?", (username,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in reels]
