import sqlite3
import hashlib
from datetime import datetime
import spacy
import praw
import os

conn = sqlite3.connect('reddit_posts.db')
c = conn.cursor()
query = '''
    SELECT content FROM posts;
    '''
    
c.execute(query)
posts = c.fetchall()

conn.close()



# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")
for post in posts:
    text = post[0]
    if len(text) == 0:
        continue

    doc = nlp(text)
    for entity in doc.ents:
        print(entity.text, entity.label_)