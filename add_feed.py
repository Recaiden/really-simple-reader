#!/usr/bin/python

import sys

DB_FEEDS = "rss/feeds.db"

def add_feed(feed_name, url):
    #TODO check for duplicates
    listing = open(DB_FEEDS, 'a+')
    listing.write(feed_name+"|"+url+"\n")
    listing.close()
    
    touch = open("rss/"+feed_name+".db", "w+")
    touch.close()

if __name__=="__main__":
    feed_name = sys.argv[1]
    url = sys.argv[2]
    add_feed(feed_name, url)
