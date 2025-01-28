import logging
from .database import get_db_connection
from .scraper_functions import scrape_reels  # Import scrape_reels from the new file

logging.basicConfig(level=logging.DEBUG)


def scrape_all_users():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all registered users
    users = cursor.execute("SELECT id, username FROM users").fetchall()

    # Scrape data for each user
    for user in users:
        user_id = user["id"]
        username = user["username"]
        logging.debug(f"Scraping data for user: {username}")

        try:
            # Use scrape_reels to fetch Reels data for the user
            data = scrape_reels(username)
            for reel in data:
                cursor.execute(
                    """
                    INSERT INTO reels (user_id, reel_id, views, likes, comments)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        reel["reel_id"],
                        reel["views"],
                        reel["likes"],
                        reel["comments"],
                    ),
                )
        except Exception as e:
            logging.error(f"Error scraping data for {username}: {e}")

    # Commit and close the database connection
    conn.commit()
    conn.close()
    logging.debug("Scraping completed for all users.")
