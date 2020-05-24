#!/usr/bin/python

import os
import socket
import logging

from flask import Flask, request, redirect
from flask import render_template

app = Flask(__name__)

logger = logging.getLogger('gunicorn.error')

class InMemoryBids:
    def __init__(self):
        self.bids = []
    
    def highest(self):
        return max(self.bids, default=0)

    def add_bid(self, bid):
        self.bids.append(bid)


class RedisBids:
    def __init__(self, host='localhost'):
        import redis
        if "REDIS_AUTH_TOKEN" in os.environ:
            self.r = redis.Redis(host=host, port=6379, db=0, password=os.getenv("REDIS_AUTH_TOKEN"))
        else:   
            self.r = redis.Redis(host=host, port=6379, db=0)
    
    def highest(self):
        return max(map(int, self.r.lrange( "bids", 0, -1 )), default=0)

    def add_bid(self, bid):
        self.r.lpush("bids", bid)  


def create_bids():
    if "REDIS_HOST" in os.environ:
        logger.info("Using redis backend on " + os.getenv("REDIS_HOST"))
        return RedisBids(os.getenv("REDIS_HOST"))
    else:
        logger.info("Using inmemory bid store")
        return InMemoryBids()

def get_hostname():   
    return socket.gethostname()

bids = create_bids()

@app.route("/")
def index():
    hostname = get_hostname()
    return render_template("index.html", hostname=hostname, highest=bids.highest())

@app.route("/bid", methods=["POST"])
def bid():
    bid = int(request.form['bid'])
    bids.add_bid(bid)
    return index()


