#!/usr/bin/env python3.6
"""Serve Humidity information via Flask"""

from flask import Flask

from redis_connection import RedisConnection

app = Flask(__name__)
rconn = RedisConnection()


@app.route("/")
def home_page():
   humidities = rconn.retrieve(10)
   humidity = round(sum(humidities)/len(humidities), 2)
   return f"<h1>Humidity {humidity}%</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
