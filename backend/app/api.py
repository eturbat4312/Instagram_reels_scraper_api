from flask import Flask, request, jsonify
from .scraper import scrape_all_users
from .database import get_db_connection
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


# Add a username to track
@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.json.get("username")
    if not username:
        return jsonify({"status": "error", "message": "Username is required."}), 400

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        return jsonify(
            {"status": "success", "message": f"User {username} added successfully."}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()


# Get Reels data with filters and sorting
@app.route("/reels", methods=["GET"])
def get_reels():
    username = request.args.get("username")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    sort_by = request.args.get("sort_by", "views")  # Default sorting by views

    # Validate required parameters
    if not username:
        return jsonify({"status": "error", "message": "Username is required"}), 400

    if not start_date or not end_date:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Both start_date and end_date are required",
                }
            ),
            400,
        )

    # Validate sort_by field
    valid_sort_fields = ["views", "likes", "comments", "timestamp"]
    if sort_by not in valid_sort_fields:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Invalid sort_by field. Must be one of {valid_sort_fields}",
                }
            ),
            400,
        )

    # Extend end_date to include full day
    if len(end_date) == 10:  # If the date is without time, add the end of day time
        end_date += " 23:59:59"

    conn = get_db_connection()
    try:
        query = """
            SELECT r.*, u.username
            FROM reels r
            JOIN users u ON r.user_id = u.id
            WHERE LOWER(u.username) = LOWER(?) AND r.timestamp BETWEEN ? AND ?
            ORDER BY r.{} DESC
        """.format(
            sort_by
        )

        logging.debug(
            f"Executing query: {query} with params: {username}, {start_date}, {end_date}"
        )
        rows = conn.execute(query, (username, start_date, end_date)).fetchall()

        # Transform results into JSON-serializable format
        results = [dict(row) for row in rows]
        return jsonify(results)

    except Exception as e:
        logging.error(f"Error in /reels endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()


# Manually trigger scraping for all users
@app.route("/scrape_all", methods=["POST"])
def scrape_all():
    try:
        scrape_all_users()
        return jsonify(
            {"status": "success", "message": "Scraping complete for all users."}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
