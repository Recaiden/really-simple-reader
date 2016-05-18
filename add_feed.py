#!/usr/bin/python

import sys

DB_FEEDS = "rss/feeds.db"

feed_name = sys.argv[1]
url = sys.argv[2]

listing = open(DB_FEEDS, 'a+')
listing.write(feed_name+"|"+url+"\n")
listing.close()
    
touch = open("rss/"+feed_name+".db", "w+")
touch.close()
