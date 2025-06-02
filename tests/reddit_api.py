import praw
import os

reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    password=os.getenv("password"),
    user_agent="testscript by u/fakebot3",
    username="B-B8",
)

print(reddit.user.me())