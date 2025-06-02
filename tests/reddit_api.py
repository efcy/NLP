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

subreddits = reddit.subreddits.search("robotics")

for subreddit in subreddits:
    #print(subreddit.fullname)
    print(subreddit.display_name)
    for submission in subreddit.hot(limit=100):
        print(f"\t{submission.title}")
        print(submission.selftext)
        print(submission.permalink)
    
    quit()