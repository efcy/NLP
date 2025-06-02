import sqlite3
import hashlib
from datetime import datetime
import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    password=os.getenv("password"),
    user_agent="testscript by u/fakebot3",
    username="B-B8",
)

def get_or_create_subreddit(conn, display_name):
    """Get subreddit ID or create if it doesn't exist"""
    c = conn.cursor()
    c.execute("SELECT id FROM subreddits WHERE display_name = ?", (display_name,))
    result = c.fetchone()
    
    if result:
        return result[0]
    else:
        c.execute("INSERT INTO subreddits (name, display_name) VALUES (?, ?)",
                 (display_name.lower(), display_name))
        conn.commit()
        return c.lastrowid
    

subreddits = reddit.subreddits.search("robotics")