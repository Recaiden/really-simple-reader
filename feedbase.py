#!/usr/bin/python

import time
import sys
from subprocess import check_output
import webbrowser

NEW_TAB_FLAG = 2

import feedparser

db = "global that should be refactored"
limit = 12 * 60 * 60 * 1000 # 12 hours, in milliseconds
#limit = 1000

DB_FEEDS = "rss/feeds.db"

# function to get the current time
timeCurrentMilli = lambda: int(round(time.time() * 1000))
tsCurrent = timeCurrentMilli()

def open_item(url):
    webbrowser.open(url, NEW_TAB_FLAG)

def postExists(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

def postHasExpired(title):
    with open(db, 'r+') as database:
        for line in database:
            if title in line:
                ts = long(line.split('|', 1)[1])
                if tsCurrent - ts > limit:
                    return True
    return False

# Gather up a list of feeds to poll
listFeeds = []
with open(DB_FEEDS, 'r+') as database:
    for feed in database:
        title = feed.split("|")[0]
        url = feed.split("|")[1].strip()
        listFeeds.append((title,url))
            
# Loop through each subscribed feed.
for listing in listFeeds:
    feed = feedparser.parse(listing[1])
    feed_name = listing[0]
    db = "rss/"+listing[0]+".db"

    posts_to_print = []
    posts_to_skip = []

    for post in feed.entries:
        # TODO check the time
        title = post.title
        if postHasExpired(title):
            posts_to_skip.append(title)
        else:
            posts_to_print.append(title)
    
    # Add all new posts to the db.
    f = open(db, 'a+')
    for title in posts_to_print:
        if not postExists(title):
            f.write(title + "|" + str(tsCurrent) + "\n")
    f.close
    
    # output all of the new posts

    print("\n" + time.strftime("%a, %b %d %I:%M %p") + ' - ' + feed_name)
    print("-----------------------------------------\n")
    for title in posts_to_print:
        print(title) # already appends a newline
