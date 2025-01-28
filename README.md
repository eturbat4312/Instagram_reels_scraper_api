# **Instagram Reels Monitor (Work in Progress)**

This project is a backend service for tracking public Instagram Reels data, such as views, likes, and comments, for multiple users. It uses Python, Flask, and SQLite, with Instaloader for scraping public Instagram data.

---

## **Features**

- Add Instagram usernames to track their Reels data.
- Scrape Reels information, including views, likes, comments, and timestamps.
- Store Reels data in an SQLite database.
- Dockerized setup for easy deployment and isolation.

---

## **Project Structure**

```plaintext
instagram_v2/
├── backend/
│   ├── app/
│   │   ├── api.py             # Main Flask app with endpoints
│   │   ├── scraper.py         # Handles scraping logic
│   │   ├── database.py        # SQLite database utilities
│   │   ├── __init__.py        # Marks app directory as a Python module
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for building the backend service
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables for credentials
└── README.md                  # Project documentation
```
