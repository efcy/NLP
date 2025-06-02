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

def hash_post(title, content):
    """Create a hash of the post content for duplicate detection"""
    combined = f"{title}{content}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()

def store_post(conn, subreddit_id, title, content, permalink, post_hash):
    """Store a post if it doesn't already exist"""
    c = conn.cursor()
    
    # Check if post already exists
    c.execute("SELECT id FROM posts WHERE post_hash = ?", (post_hash,))
    if c.fetchone() is None:
        c.execute('''INSERT INTO posts 
                    (subreddit_id, title, content, permalink, post_hash, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (subreddit_id, title, content, permalink, post_hash, datetime.now()))
        conn.commit()
        return True
    return False

def fetch_and_store_posts(reddit):
    """Fetch posts from robotics subreddits and store them in the database"""
    conn = sqlite3.connect('reddit_posts.db')
    
    subreddits = reddit.subreddits.search("robotics")
    total_new = 0
    
    for subreddit in subreddits:
        print(f"Processing subreddit: {subreddit.display_name}")
        
        subreddit_id = get_or_create_subreddit(conn, subreddit.display_name)
        new_posts = 0
        
        for submission in subreddit.hot(limit=100):
            # Skip stickied posts
            if submission.stickied:
                continue
                
            post_hash = hash_post(submission.title, submission.selftext)
            
            if store_post(conn, subreddit_id, submission.title, 
                         submission.selftext, submission.permalink, post_hash):
                new_posts += 1
        
        print(f"  Added {new_posts} new posts")
        total_new += new_posts
    
    conn.close()
    print(f"\nTotal new posts added: {total_new}")

fetch_and_store_posts(reddit)