import sqlite3


def initialize_database():
    """Create the database and tables if they don't exist"""
    conn = sqlite3.connect('reddit_posts.db')
    c = conn.cursor()
    
    # Create subreddits table
    c.execute('''CREATE TABLE IF NOT EXISTS subreddits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  display_name TEXT)''')
    
    # Create posts table
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  subreddit_id INTEGER,
                  title TEXT,
                  content TEXT,
                  permalink TEXT,
                  post_hash TEXT UNIQUE,
                  timestamp DATETIME,
                  FOREIGN KEY(subreddit_id) REFERENCES subreddits(id))''')
    
    conn.commit()
    conn.close()

initialize_database()