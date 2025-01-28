import requests
import logging
import sqlite3

# Your RapidAPI Key
RAPIDAPI_KEY = "be57d0c471msh8e29a2de1975ed9p130ecdjsn625b59a46fc0"


# Base URL for the API
BASE_URL = "https://instagram-scraper-20252.p.rapidapi.com/v1.2/posts"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database path
DATABASE_PATH = "backend/app/database.db"


def get_db_connection():
    """
    Create and return a connection to the SQLite database.
    """
    logging.debug(f"Connecting to database at: {DATABASE_PATH}")
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.set_trace_callback(print)  # Logs every SQL query
    return conn


def scrape_reels(username):
    """
    Fetch reels (or video posts) data for a public Instagram account using RapidAPI.
    Handles pagination to fetch all available reels.
    """
    headers = {
        "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
    }
    params = {"username_or_id_or_url": username}
    reels = []

    try:
        while True:
            # Make the API request
            logging.debug(f"Making request to: {BASE_URL} with params: {params}")
            response = requests.get(BASE_URL, headers=headers, params=params)
            logging.debug(f"Response Status: {response.status_code}")
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            posts = data.get("data", {}).get("items", [])
            logging.debug(
                f"Posts extracted for {username}: {len(posts)} posts"
            )  # Log count per page

            # Process each post
            for post in posts:
                if post.get("play_count") is not None:  # Video/Reel detection
                    reels.append(
                        {
                            "reel_id": post.get("id", "unknown"),
                            "views": post.get("play_count", 0),
                            "likes": post.get("like_count", 0),
                            "comments": post.get("comment_count", 0),
                            "taken_at": post.get("taken_at", None),  # API timestamp
                        }
                    )

            # Check for pagination
            next_cursor = data.get("data", {}).get("paging", {}).get("next")
            if not next_cursor:
                logging.debug("No next cursor found, stopping pagination.")
                break

            params["cursor"] = next_cursor  # Update params with the next page cursor
            logging.debug(f"Fetching next page with cursor: {next_cursor}")

        logging.debug(
            f"Total Reels extracted for {username}: {len(reels)}"
        )  # Log total count
        return reels

    except Exception as e:
        logging.error(f"Error fetching reels for {username}: {e}")
        return []


def scrape_all_users():
    """
    Scrape Reels data for all users in the database.
    Handles duplicate prevention using INSERT OR IGNORE.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    users = cursor.execute("SELECT id, username FROM users").fetchall()
    for user in users:
        user_id = user["id"]
        username = user["username"]
        logging.debug(f"Scraping data for user: {username}")

        reels_data = scrape_reels(username)
        logging.debug(f"Reels data returned for {username}: {reels_data}")

        for reel in reels_data:
            try:
                logging.debug(f"Inserting reel into database: {reel}")
                cursor.execute(
                    """
                    INSERT INTO reels (user_id, reel_id, views, likes, comments, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        reel["reel_id"],
                        reel["views"],
                        reel["likes"],
                        reel["comments"],
                        reel.get("taken_at", "CURRENT_TIMESTAMP"),
                    ),
                )
            except sqlite3.IntegrityError as e:
                logging.error(f"Duplicate entry skipped for {reel}: {e}")
            except Exception as e:
                logging.error(f"Error inserting reel {reel}: {e}")

    conn.commit()
    logging.debug("Data committed to the database.")
    conn.close()
