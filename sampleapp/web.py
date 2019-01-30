#!/usr/bin/python

import os

from flask import Flask, request, redirect
from flask import render_template

app = Flask(__name__)


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
        self.r = redis.Redis(host=host, port=6379, db=0)
    
    def highest(self):
        return max(map(int, self.r.lrange( "bids", 0, -1 )), default=0)

    def add_bid(self, bid):
        self.r.lpush("bids", bid)  


def create_bids():
    if "REDIS_HOST" in os.environ:
        return RedisBids(os.getenv("REDIS_HOST"))
    else:
        return InMemoryBids()

bids = create_bids()

@app.route("/")
def index():
    return render_template("index.html", highest=bids.highest())

@app.route("/bid", methods=["POST"])
def bid():
    bid = int(request.form['bid'])
    bids.add_bid(bid)
    return redirect("/")


