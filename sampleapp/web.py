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


class MysqlBids:
    def __init__(self, host="localhost", password="password123"):
        self.host = host
        self.password = password
        self.bids = []
    
    def connect(self):
        import mysql.connector
        return mysql.connector.connect(user="bidapp", password=self.password, host=self.host, port="3306", database="bidapp")

    def highest(self):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(bid) FROM bid")
        row = cursor.fetchone()
        connection.close()
        return 0 if row[0] == None else row[0]

    def add_bid(self, bid):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO bid (bid) VALUES (%s)", (int(bid),))
        connection.commit()
        connection.close()


class RedisBids:
    def __init__(self, host='localhost'):
        import redis
        if "REDIS_AUTH_TOKEN" in os.environ:
            logger.info("Using auth token " + os.getenv("REDIS_AUTH_TOKEN"))
            self.r = redis.Redis(host=host, port=6379, db=0, password=os.getenv("REDIS_AUTH_TOKEN"), ssl=True)
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
    elif "MYSQL_HOST" in os.environ:
        logger.info("Using mysql backend on " + os.getenv("MYSQL_HOST"))
        return MysqlBids(os.getenv("MYSQL_HOST"), os.getenv("MYSQL_PASSWORD"))
    else:
        logger.info("Using inmemory bid store")
        return InMemoryBids()

def get_hostname():   
    return socket.gethostname()

bids = create_bids()

@app.route("/", methods=["GET"])
def index():
    hostname = get_hostname()
    return render_template("index.html", hostname=hostname, highest=bids.highest())

@app.route("/", methods=["POST"])
def bid():
    bid = int(request.form['bid'])
    bids.add_bid(bid)
    return index()


